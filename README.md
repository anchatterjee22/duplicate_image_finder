# Duplicate Image Finder

A Python-based web application that detects duplicate images, even when they are rotated. The application uses perceptual hashing to identify similar images and provides a modern web interface for easy use.

## Features

- **Duplicate Detection**: Identifies duplicate images using perceptual hashing
- **Rotation Detection**: Detects duplicates even when images are rotated (90°, 180°, 270°)
- **Web Interface**: Modern, responsive HTML/CSS frontend with drag-and-drop support
- **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, BMP, and TIFF formats
- **Batch Processing**: Upload up to 25 images (max 50MB total) at once for analysis
- **Visual Results**: Displays duplicate groups with thumbnail previews
- **Unique Images Tab**: View all non-duplicate images in a separate tab

## How It Works

The application uses the `imagehash` library to calculate perceptual hashes of images. For each uploaded image, it generates hashes for:
- The original image
- 90° rotation
- 180° rotation  
- 270° rotation

This allows the system to detect duplicates regardless of orientation. Images with matching hashes are grouped together as duplicates.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**
2. **Navigate to the project directory**:
   ```bash
   cd image_finder
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Web Application

1. **Start the Flask server**:
   ```bash
   python app.py
   ```

2. **Open your web browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Upload images**:
   - Drag and drop up to 25 images (max 50MB total) onto the upload area, or
   - Click "Browse Files" to select images manually

4. **Click "Find Duplicates"** to analyze the images

5. **View results** showing duplicate groups with thumbnails

6. **Switch between tabs** to view duplicates or unique images

### Command Line Usage

You can also use the duplicate finder directly from the command line:

```bash
python duplicate_finder.py image1.jpg image2.png image3.jpg
```

This will output duplicate groups to the console.

## File Structure

```
image_finder/
├── app.py                 # Flask web application
├── duplicate_finder.py    # Core duplicate detection logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   └── css/
│       └── style.css     # CSS styling
└── uploads/              # Temporary upload directory (auto-created)
```

## Technical Details

### Dependencies

- **Flask**: Web framework for the application
- **Pillow (PIL)**: Image processing and manipulation
- **imagehash**: Perceptual hashing algorithms for image comparison
- **numpy**: Numerical computing support
- **Werkzeug**: WSGI utilities for Flask

### Algorithms

- **Perceptual Hashing**: Uses difference hashing (dhash) for robust image comparison
- **Rotation Detection**: Generates hashes for multiple orientations
- **Similarity Matching**: Groups images with identical hashes

### Performance

- **Memory Efficient**: Processes images one at a time
- **Fast Analysis**: Perceptual hashing is computationally lightweight
- **Scalable**: Can handle various image sizes and formats

## Limitations

- Maximum file size: 50MB total for all images
- Maximum images: 25 per analysis session
- Supported formats: PNG, JPG, JPEG, GIF, BMP, TIFF
- Rotation detection limited to 90° increments

## Troubleshooting

### Common Issues

1. **"No module named 'imagehash'"**
   - Run: `pip install -r requirements.txt`

2. **"PIL module not found"**
   - Run: `pip install Pillow`

3. **Images not loading**
   - Check file format support
   - Ensure total file size is under 50MB

4. **Server won't start**
   - Check if port 5000 is available
   - Ensure all dependencies are installed

### Performance Tips

- Use smaller image files for faster processing
- Close other applications to free up memory
- Ensure adequate disk space for temporary files

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please check the troubleshooting section above or create an issue in the project repository.
