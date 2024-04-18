import asyncio
from aiopath import AsyncPath
from aioshutil import copyfile

async def save_files(from_dir: AsyncPath, to_dir: AsyncPath):
    try:
        await to_dir.mkdir(parents=True, exist_ok=True)

        async for file_path in from_dir.iterdir():
            try:
                if (await file_path.is_file()):
                    extension = file_path.suffix
                    subdir_path = to_dir / extension.replace('.', '')
                    await subdir_path.mkdir(parents=True, exist_ok=True)

                    destination_path = subdir_path / file_path.name
                    await copy_file(file_path, destination_path)

                elif (await file_path.is_dir()):
                    await save_files(file_path, to_dir)

            except (PermissionError, FileNotFoundError) as e:
                print(f"Error processing file {file_path}: {e}")

    except (PermissionError, FileNotFoundError) as e:
        print(f"Error accessing destination directory {to_dir}: {e}")

async def copy_file(source_path: AsyncPath, destination_path: AsyncPath):
    try:
        destination_folder = destination_path.parent
        await destination_folder.mkdir(parents=True, exist_ok=True)
        await copyfile(source_path, destination_path)

        print(f"Successfully copied '{source_path}' to '{destination_path}'")

    except (PermissionError, FileNotFoundError) as e:
        print(f"Error copying file {source_path} to {destination_path}: {e}")

async def main():
    from_dir=AsyncPath('main_dir')
    to_dir = AsyncPath('kari')
    await save_files(from_dir, to_dir)

if __name__ == '__main__':
    asyncio.run(main())

