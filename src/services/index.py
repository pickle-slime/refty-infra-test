from schemas.requests.index import UpdateImageRequest
from core.config import settings

import logging
import aiohttp
import base64
import re

GITHUB_TOKEN = settings.env.get_variable("GITHUB_TOKEN")
REPO = settings.env.get_variable("REPOSITORY_FORK")
USERNAME = settings.env.get_variable("GITHUB_USERNAME")
BRANCH = settings.env.get_variable("REPOSITORY_BRANCH")

API_BASE = f"https://api.github.com/repos/{USERNAME}/{REPO}"

logger = logging.getLogger(__name__)

async def update_image_service(request: UpdateImageRequest) -> tuple[int, str, list[str]]:
    image_prefix = f"image: {request.image}:"
    new_image = f"{image_prefix}{request.version}"
    updated_files: list[str] = []

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            # branch info
            branch_url = f"{API_BASE}/branches/{BRANCH}"
            async with session.get(branch_url, headers=headers) as branch_resp:
                if branch_resp.status != 200:
                    detail = await branch_resp.text()
                    raise RuntimeError(f"Failed to fetch branch info: {detail}")
                branch_data = await branch_resp.json()
                tree_sha = branch_data["commit"]["commit"]["tree"]["sha"]

            # full tree
            tree_url = f"{API_BASE}/git/trees/{tree_sha}?recursive=1"
            async with session.get(tree_url, headers=headers) as tree_resp:
                if tree_resp.status != 200:
                    detail = await tree_resp.text()
                    raise RuntimeError(f"Failed to fetch tree: {detail}")
                tree_data = await tree_resp.json()

            # all YAML files
            yaml_files = [
                item for item in tree_data["tree"]
                if item["path"].endswith((".yml", ".yaml")) and item["type"] == "blob"
            ]

            if not yaml_files:
                logger.warning("No YAML files found in the repo.")
                return 404, "No YAML files found in the repo.", []

            # process each file
            for file in yaml_files:
                path = file["path"]
                file_url = f"{API_BASE}/contents/{path}?ref={BRANCH}"

                # file content
                async with session.get(file_url, headers=headers) as file_resp:
                    if file_resp.status != 200:
                        logger.warning(f"Failed to fetch file {path}: {file_resp.status}")
                        continue
                    file_data = await file_resp.json()

                try:
                    raw_content = base64.b64decode(file_data["content"]).decode()
                except Exception as e:
                    logger.error(f"Failed to decode base64 content for {path}: {e}")
                    continue

                # replace image version
                if image_prefix not in raw_content:
                    continue

                updated_content = re.sub(
                    rf"{re.escape(image_prefix)}[\w\-]+",
                    new_image,
                    raw_content
                )

                if updated_content == raw_content:
                    continue

                # commit changes
                payload = {
                    "message": f"Update image version in {path} to {request.version}",
                    "content": base64.b64encode(updated_content.encode()).decode(),
                    "sha": file_data["sha"],
                    "branch": BRANCH,
                }

                async with session.put(file_url, headers=headers, json=payload) as update_resp:
                    if update_resp.status not in (200, 201):
                        error_text = await update_resp.text()
                        logger.error(f"Failed to update {path}: {update_resp.status} - {error_text}")
                        continue

                    updated_files.append(path)
                    logger.info(f"Updated {path}")

    except aiohttp.ClientError as e:
        logger.exception(f"HTTP error during GitHub interaction: {e}")
        raise RuntimeError("Network issue while communicating with GitHub")

    except Exception as e:
        logger.exception(f"An unexpected error: {e}")
        raise RuntimeError(f"An unexpected error occurred: {e}")

    return 200, "success", updated_files

