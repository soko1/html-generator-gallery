#!/usr/bin/env python3

import os
import base64

# Get a list of supported image files in the current directory and sort them
def get_image_files():
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    return sorted(f for f in os.listdir() if f.lower().endswith(supported_formats))

# Generate HTML code
def generate_html(file_list):
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Gallery</title>
        <style>
            body {
                background-color: #1e1e1e;
                color: #fff;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                margin: 0;
                padding: 0;
            }
            .thumbnail {
                margin: 10px;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .thumbnail:hover {
                transform: scale(1.05);
            }
            img {
                max-width: 200px;
                max-height: 150px;
                border: 2px solid #fff;
            }
            .lightbox {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.9);
                justify-content: center;
                align-items: center;
            }
            .lightbox img {
                max-width: 90%;
                max-height: 90%;
            }
            .arrow {
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                font-size: 2em;
                color: white;
                cursor: pointer;
            }
            .left-arrow {
                left: 20px;
            }
            .right-arrow {
                right: 20px;
            }
        </style>
    </head>
    <body>
    <div class="lightbox" id="lightbox" onclick="this.style.display='none'">
        <div class="arrow left-arrow" onclick="changeImage(-1); event.stopPropagation();">&#10094;</div>
        <div class="arrow right-arrow" onclick="changeImage(1); event.stopPropagation();">&#10095;</div>
        <img id="lightbox-img" src="">
    </div>
    '''

    html_content += '''
    <script>
        let images = ''' + str(file_list) + ''';
        let currentIndex = 0;

        function showImage(index) {
            currentIndex = index;
            document.getElementById('lightbox-img').src = images[index];
            document.getElementById('lightbox').style.display = 'flex';
        }

        function changeImage(direction) {
            currentIndex += direction;
            if (currentIndex < 0) currentIndex = images.length - 1;
            if (currentIndex >= images.length) currentIndex = 0;
            showImage(currentIndex);
        }

        document.addEventListener('keydown', function(event) {
            if (document.getElementById('lightbox').style.display === 'flex') {
                if (event.key === 'ArrowLeft') {
                    changeImage(-1);
                }
                if (event.key === 'ArrowRight') {
                    changeImage(1);
                }
            }
        });
    </script>
    '''

    for filename in file_list:
        encoded_image = base64.b64encode(open(filename, 'rb').read()).decode()
        html_content += f'''
        <div class="thumbnail" onclick="showImage({file_list.index(filename)})">
            <img src="data:image/jpeg;base64,{encoded_image}" alt="{filename}">
        </div>
        '''

    html_content += '''
    </body>
    </html>
    '''

    return html_content

# Main function
def main():
    image_files = get_image_files()
    if not image_files:
        print("No image files found in the current directory.")
        return

    html_output = generate_html(image_files)

    with open("gallery.html", "w", encoding="utf-8") as f:
        f.write(html_output)

    print("HTML page with the gallery created: gallery.html")

if __name__ == "__main__":
    main()

