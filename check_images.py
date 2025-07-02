#!/usr/bin/env python3
"""
이미지 파일 검증 도구
images 폴더의 모든 이미지 파일을 검사하여 손상된 파일을 찾습니다.
"""

import os
from pathlib import Path
from PIL import Image

def check_images_folder():
    """images 폴더의 모든 이미지를 검증"""
    image_folder = "images"
    
    if not os.path.exists(image_folder):
        print("❌ images 폴더가 없습니다.")
        return
    
    print("🔍 이미지 파일 검증을 시작합니다...\n")
    
    supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    valid_images = []
    invalid_images = []
    
    for file_path in Path(image_folder).iterdir():
        if file_path.is_file():
            file_ext = file_path.suffix.lower()
            
            if file_ext in supported_extensions:
                try:
                    with Image.open(file_path) as img:
                        img.verify()  # 이미지 검증
                    
                    # 다시 열어서 정보 확인
                    with Image.open(file_path) as img:
                        width, height = img.size
                        mode = img.mode
                        format_name = img.format
                    
                    print(f"✅ {file_path.name}")
                    print(f"   크기: {width}x{height}, 모드: {mode}, 형식: {format_name}")
                    valid_images.append(file_path.name)
                    
                except Exception as e:
                    print(f"❌ {file_path.name}")
                    print(f"   오류: {str(e)}")
                    invalid_images.append(file_path.name)
            
            elif file_ext:
                print(f"⚠️  {file_path.name} (지원하지 않는 형식)")
            
    print(f"\n📊 검증 결과:")
    print(f"✅ 유효한 이미지: {len(valid_images)}개")
    print(f"❌ 손상된 이미지: {len(invalid_images)}개")
    
    if invalid_images:
        print(f"\n🔧 손상된 파일 목록:")
        for img in invalid_images:
            print(f"   - {img}")
        print("\n💡 손상된 파일을 다시 다운로드하거나 다른 파일로 교체하세요.")
    
    if len(valid_images) < 50:
        print(f"\n⚠️  현재 {len(valid_images)}개의 이미지가 있습니다. 50개까지 추가할 수 있습니다.")
    
    print(f"\n✨ 지원되는 형식: {', '.join(supported_extensions)}")

if __name__ == "__main__":
    check_images_folder()
