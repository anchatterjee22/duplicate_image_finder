import os
import hashlib
import imagehash
from PIL import Image
import numpy as np
from collections import defaultdict
import json
import base64
from io import BytesIO

class DuplicateImageFinder:
    def __init__(self):
        self.image_hashes = {}
        self.duplicate_groups = []
        
    def calculate_image_hash(self, image_path):
        """Calculate perceptual hash of an image"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Calculate perceptual hash (dhash is good for detecting rotations)
                hash_value = imagehash.dhash(img)
                return str(hash_value)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None
    
    def calculate_rotated_hashes(self, image_path):
        """Calculate hashes for different rotations of the image"""
        try:
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                hashes = []
                # Original image
                hashes.append(str(imagehash.dhash(img)))
                
                # Rotate 90, 180, 270 degrees
                for angle in [90, 180, 270]:
                    rotated = img.rotate(angle, expand=True)
                    hashes.append(str(imagehash.dhash(rotated)))
                
                return hashes
        except Exception as e:
            print(f"Error processing rotations for {image_path}: {e}")
            return None
    
    def find_duplicates(self, image_paths, similarity_threshold=5):
        """Find duplicate images based on perceptual hashing"""
        self.image_hashes = {}
        self.duplicate_groups = []
        
        # Calculate hashes for all images including rotations
        for image_path in image_paths:
            if os.path.exists(image_path):
                rotated_hashes = self.calculate_rotated_hashes(image_path)
                if rotated_hashes:
                    self.image_hashes[image_path] = rotated_hashes
        
        # Group images by similar hashes
        hash_groups = defaultdict(list)
        
        for image_path, hashes in self.image_hashes.items():
            for hash_val in hashes:
                hash_groups[hash_val].append(image_path)
        
        # Find duplicates
        processed_images = set()
        
        for hash_val, image_list in hash_groups.items():
            if len(image_list) > 1:
                # Check if any of these images haven't been processed yet
                unprocessed = [img for img in image_list if img not in processed_images]
                if len(unprocessed) > 1:
                    duplicate_group = {
                        'images': unprocessed,
                        'hash': hash_val,
                        'count': len(unprocessed)
                    }
                    self.duplicate_groups.append(duplicate_group)
                    
                    # Mark these images as processed
                    for img in unprocessed:
                        processed_images.add(img)
        
        return self.duplicate_groups
    
    def get_image_base64(self, image_path):
        """Convert image to base64 for HTML display"""
        try:
            with Image.open(image_path) as img:
                # Resize image for display (max 200x200)
                img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                return f"data:image/png;base64,{img_str}"
        except Exception as e:
            print(f"Error converting {image_path} to base64: {e}")
            return None
    
    def generate_report(self, image_paths):
        """Generate a comprehensive report of duplicates"""
        duplicates = self.find_duplicates(image_paths)
        
        # Get all duplicate image paths
        duplicate_paths = set()
        for group in duplicates:
            for image_path in group['images']:
                duplicate_paths.add(image_path)
        
        # Get unique images (not in any duplicate group)
        unique_paths = [path for path in image_paths if path not in duplicate_paths]
        
        report = {
            'total_images': len(image_paths),
            'duplicate_groups': [],
            'unique_images': len(unique_paths),
            'unique_images_list': []
        }
        
        # Process duplicate groups
        for group in duplicates:
            group_info = {
                'count': group['count'],
                'images': []
            }
            
            for image_path in group['images']:
                image_info = {
                    'path': image_path,
                    'filename': os.path.basename(image_path),
                    'base64': self.get_image_base64(image_path)
                }
                group_info['images'].append(image_info)
            
            report['duplicate_groups'].append(group_info)
        
        # Process unique images
        for image_path in unique_paths:
            image_info = {
                'path': image_path,
                'filename': os.path.basename(image_path),
                'base64': self.get_image_base64(image_path)
            }
            report['unique_images_list'].append(image_info)
        
        return report

def main():
    """Main function for command line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python duplicate_finder.py <image_path1> <image_path2> ...")
        return
    
    image_paths = sys.argv[1:]
    finder = DuplicateImageFinder()
    
    print(f"Analyzing {len(image_paths)} images...")
    duplicates = finder.find_duplicates(image_paths)
    
    if not duplicates:
        print("No duplicates found!")
    else:
        print(f"Found {len(duplicates)} duplicate groups:")
        for i, group in enumerate(duplicates, 1):
            print(f"\nGroup {i} ({group['count']} images):")
            for image_path in group['images']:
                print(f"  - {os.path.basename(image_path)}")

if __name__ == "__main__":
    main()
