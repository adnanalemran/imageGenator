// DOM Elements
const generatorForm = document.getElementById('generatorForm');
const promptInput = document.getElementById('prompt');
const charCount = document.getElementById('charCount');
const preview = document.getElementById('preview');
const previewImage = document.getElementById('previewImage');
const loadingIndicator = document.getElementById('loadingIndicator');
const downloadBtn = document.getElementById('downloadBtn');
const shareBtn = document.getElementById('shareBtn');
const galleryGrid = document.getElementById('galleryGrid');
const toast = document.getElementById('toast');
const toastMessage = document.getElementById('toastMessage');

// Constants
const MAX_CHARS = 500;
const API_ENDPOINT = '/api/generate';
const GALLERY_ENDPOINT = '/api/gallery';

// Character Counter
promptInput.addEventListener('input', () => {
    const count = promptInput.value.length;
    charCount.textContent = count;
    
    if (count > MAX_CHARS) {
        promptInput.classList.add('error-input');
        charCount.classList.add('text-red-500');
    } else {
        promptInput.classList.remove('error-input');
        charCount.classList.remove('text-red-500');
    }
});

// Form Submission
generatorForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (promptInput.value.length > MAX_CHARS) {
        showToast('Prompt is too long. Maximum 500 characters allowed.', 'error');
        return;
    }
    
    const formData = new FormData(generatorForm);
    const data = Object.fromEntries(formData.entries());
    
    try {
        showLoading(true);
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate image');
        }
        
        const result = await response.json();
        displayPreview(result.imageUrl);
        updateGallery();
        showToast('Image generated successfully!', 'success');
    } catch (error) {
        console.error('Error:', error);
        showToast('Failed to generate image. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
});

// Display Preview
function displayPreview(imageUrl) {
    previewImage.src = imageUrl;
    preview.classList.remove('hidden');
    preview.scrollIntoView({ behavior: 'smooth' });
}

// Loading State
function showLoading(show) {
    if (show) {
        loadingIndicator.classList.remove('hidden');
        generatorForm.classList.add('loading');
    } else {
        loadingIndicator.classList.add('hidden');
        generatorForm.classList.remove('loading');
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    toastMessage.textContent = message;
    toast.className = `fixed bottom-4 right-4 transform transition-transform duration-300 ${type}`;
    toast.classList.add('toast-show');
    
    setTimeout(() => {
        toast.classList.remove('toast-show');
        toast.classList.add('toast-hide');
    }, 3000);
}

// Download Image
downloadBtn.addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = previewImage.src;
    link.download = `generated-image-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Image downloaded successfully!', 'success');
});

// Share Image
shareBtn.addEventListener('click', async () => {
    try {
        if (navigator.share) {
            await navigator.share({
                title: 'AI Generated Image',
                text: 'Check out this AI generated image!',
                url: previewImage.src,
            });
            showToast('Image shared successfully!', 'success');
        } else {
            // Fallback for browsers that don't support Web Share API
            await navigator.clipboard.writeText(previewImage.src);
            showToast('Image URL copied to clipboard!', 'info');
        }
    } catch (error) {
        console.error('Error sharing:', error);
        showToast('Failed to share image.', 'error');
    }
});

// Gallery Management
async function updateGallery() {
    try {
        const response = await fetch(GALLERY_ENDPOINT);
        if (!response.ok) {
            throw new Error('Failed to fetch gallery');
        }
        
        const images = await response.json();
        displayGallery(images);
    } catch (error) {
        console.error('Error fetching gallery:', error);
        showToast('Failed to update gallery.', 'error');
    }
}

function displayGallery(images) {
    galleryGrid.innerHTML = images.map(image => `
        <div class="gallery-item">
            <img src="${image.url}" alt="${image.prompt}" class="w-full h-48 object-cover">
            <div class="gallery-item-overlay">
                <div class="text-white text-center p-4">
                    <p class="text-sm mb-2">${image.prompt}</p>
                    <div class="flex justify-center space-x-2">
                        <button onclick="downloadGalleryImage('${image.url}')" 
                            class="p-2 bg-white bg-opacity-20 rounded-full hover:bg-opacity-30 transition-colors">
                            <i class="fas fa-download"></i>
                        </button>
                        <button onclick="shareGalleryImage('${image.url}')" 
                            class="p-2 bg-white bg-opacity-20 rounded-full hover:bg-opacity-30 transition-colors">
                            <i class="fas fa-share-alt"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Gallery Image Actions
async function downloadGalleryImage(url) {
    const link = document.createElement('a');
    link.href = url;
    link.download = `gallery-image-${Date.now()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Image downloaded successfully!', 'success');
}

async function shareGalleryImage(url) {
    try {
        if (navigator.share) {
            await navigator.share({
                title: 'AI Generated Image from Gallery',
                text: 'Check out this AI generated image!',
                url: url,
            });
            showToast('Image shared successfully!', 'success');
        } else {
            await navigator.clipboard.writeText(url);
            showToast('Image URL copied to clipboard!', 'info');
        }
    } catch (error) {
        console.error('Error sharing:', error);
        showToast('Failed to share image.', 'error');
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateGallery();
    
    // Add smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Error Handling
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    showToast('An unexpected error occurred. Please try again.', 'error');
});

// Responsive Design
function handleResize() {
    const width = window.innerWidth;
    if (width < 640) {
        // Mobile adjustments
        document.querySelectorAll('.gallery-item').forEach(item => {
            item.style.height = '200px';
        });
    } else {
        // Desktop adjustments
        document.querySelectorAll('.gallery-item').forEach(item => {
            item.style.height = 'auto';
        });
    }
}

window.addEventListener('resize', handleResize);
handleResize(); 