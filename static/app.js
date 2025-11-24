/**
 * Avatar Teacher Frontend Application
 * Handles UI interactions, API calls, and media playback
 */

// API base URL
const API_BASE = '/api';

// DOM elements
let avatarVideo = null;
let voiceAudio = null;
let topicListEl = null;
let welcomeScreen = null;
let playerContainer = null;
let topicTitleEl = null;
let topicTextEl = null;
let languageBadgeEl = null;
let faqSectionEl = null;
let faqListEl = null;
let currentFaqEl = null;
let faqQuestionEl = null;
let faqAnswerEl = null;
let closeFaqBtn = null;
let statusIndicator = null;
let statusText = null;
let audioError = null;

// Current state
let currentTopic = null;
let currentFaqs = [];
let currentTopicId = null;

/**
 * Initialize the application
 */
function init() {
    // Get DOM elements
    avatarVideo = document.getElementById('avatarVideo');
    voiceAudio = document.getElementById('voiceAudio');
    topicListEl = document.getElementById('topicList');
    welcomeScreen = document.getElementById('welcomeScreen');
    playerContainer = document.getElementById('playerContainer');
    topicTitleEl = document.getElementById('topicTitle');
    topicTextEl = document.getElementById('topicText');
    languageBadgeEl = document.getElementById('languageBadge');
    faqSectionEl = document.getElementById('faqSection');
    faqListEl = document.getElementById('faqList');
    currentFaqEl = document.getElementById('currentFaq');
    faqQuestionEl = document.getElementById('faqQuestion');
    faqAnswerEl = document.getElementById('faqAnswer');
    closeFaqBtn = document.getElementById('closeFaqBtn');
    statusIndicator = document.getElementById('statusIndicator');
    statusText = document.getElementById('statusText');
    audioError = document.getElementById('audioError');

    // Set up event listeners
    voiceAudio.addEventListener('play', onAudioPlay);
    voiceAudio.addEventListener('ended', onAudioEnded);
    voiceAudio.addEventListener('pause', onAudioPause);
    voiceAudio.addEventListener('error', onAudioError);
    voiceAudio.addEventListener('loadeddata', onAudioLoaded);
    closeFaqBtn.addEventListener('click', closeFaqAnswer);

    // Load topics on page load
    loadTopics();
}

/**
 * Fetch and display all topics
 */
async function loadTopics() {
    try {
        const response = await fetch(`${API_BASE}/topics`);
        if (!response.ok) {
            throw new Error('Failed to fetch topics');
        }

        const topics = await response.json();
        displayTopics(topics);
    } catch (error) {
        console.error('Error loading topics:', error);
        topicListEl.innerHTML = '<div class="error">Failed to load topics. Please refresh the page.</div>';
    }
}

/**
 * Display topics in the sidebar
 */
function displayTopics(topics) {
    if (topics.length === 0) {
        topicListEl.innerHTML = '<div class="empty">No topics available</div>';
        return;
    }

    topicListEl.innerHTML = '';
    topics.forEach(topic => {
        const button = document.createElement('button');
        button.className = 'topic-button';
        button.dataset.topicId = topic.id;
        button.innerHTML = `
            <span class="topic-title">${escapeHtml(topic.title)}</span>
            <span class="topic-lang">${getLanguageLabel(topic.language)}</span>
        `;
        button.addEventListener('click', () => selectTopic(topic.id));
        topicListEl.appendChild(button);
    });
}

/**
 * Handle topic selection
 */
async function selectTopic(topicId) {
    try {
        // Show loading state
        showLoading(true);
        
        // Update active topic button
        highlightActiveTopic(topicId);

        // Fetch topic details with FAQs
        const response = await fetch(`${API_BASE}/topics/${topicId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch topic details');
        }

        const topic = await response.json();
        currentTopic = topic;
        currentFaqs = topic.faqs || [];
        currentTopicId = topicId;

        // Display topic
        displayTopic(topic);
        
        // Hide welcome screen, show player
        welcomeScreen.style.display = 'none';
        playerContainer.style.display = 'flex';
        
        // Hide loading
        showLoading(false);

        // Start playing video and audio
        playTopicMedia(topic);
    } catch (error) {
        console.error('Error selecting topic:', error);
        showLoading(false);
        showError('Failed to load topic. Please try again.');
    }
}

/**
 * Display topic content
 */
function displayTopic(topic) {
    // Set title and language
    topicTitleEl.textContent = topic.title;
    languageBadgeEl.textContent = getLanguageLabel(topic.language);
    
    // Set content text
    topicTextEl.innerHTML = `<p>${escapeHtml(topic.content_text)}</p>`;

    // Display FAQs
    displayFAQs(topic.faqs);

    // Hide current FAQ answer if showing
    currentFaqEl.style.display = 'none';
}

/**
 * Play topic video and audio
 */
function playTopicMedia(topic) {
    // Reset audio error message
    if (audioError) {
        audioError.style.display = 'none';
    }
    
    // Set video source
    avatarVideo.src = topic.avatar_video_url || '/static/media/avatar_loop.mp4';
    avatarVideo.loop = true;
    avatarVideo.muted = false;
    
    // Play video
    avatarVideo.play().catch(error => {
        console.error('Error playing video:', error);
        // If autoplay fails, try muted
        avatarVideo.muted = true;
        avatarVideo.play().catch(e => {
            console.error('Video playback failed:', e);
        });
    });

    // Set and play audio
    if (topic.audio_url) {
        voiceAudio.src = topic.audio_url;
        voiceAudio.load();
        
        // Small delay to ensure audio is loaded
        setTimeout(() => {
            voiceAudio.play().catch(error => {
                console.error('Error playing audio:', error);
                if (audioError) {
                    audioError.style.display = 'block';
                }
            });
        }, 100);
    } else {
        console.warn('No audio URL provided for this topic');
        if (audioError) {
            audioError.style.display = 'block';
        }
    }
}

/**
 * Display FAQs as buttons
 */
function displayFAQs(faqs) {
    if (!faqs || faqs.length === 0) {
        faqSectionEl.style.display = 'none';
        return;
    }

    faqListEl.innerHTML = '';
    faqs.forEach(faq => {
        const button = document.createElement('button');
        button.className = 'faq-button';
        button.textContent = faq.question;
        button.addEventListener('click', () => selectFAQ(faq.id));
        faqListEl.appendChild(button);
    });

    // FAQs will be shown after topic audio ends
    faqSectionEl.style.display = 'none';
}

/**
 * Handle FAQ selection
 */
async function selectFAQ(faqId) {
    try {
        // Reset audio error
        if (audioError) {
            audioError.style.display = 'none';
        }
        
        // Fetch FAQ details
        const response = await fetch(`${API_BASE}/faqs/${faqId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch FAQ details');
        }

        const faq = await response.json();
        displayFAQAnswer(faq);

        // Play FAQ audio while keeping video looping
        if (faq.answer_audio_url) {
            voiceAudio.src = faq.answer_audio_url;
            voiceAudio.load();
            
            setTimeout(() => {
                voiceAudio.play().catch(error => {
                    console.error('Error playing FAQ audio:', error);
                    if (audioError) {
                        audioError.style.display = 'block';
                    }
                });
            }, 100);
        } else {
            console.warn('No audio URL for this FAQ');
        }
    } catch (error) {
        console.error('Error selecting FAQ:', error);
        showError('Failed to load FAQ. Please try again.');
    }
}

/**
 * Display FAQ answer
 */
function displayFAQAnswer(faq) {
    faqQuestionEl.textContent = faq.question;
    faqAnswerEl.textContent = faq.answer;
    currentFaqEl.style.display = 'block';
    
    // Scroll to FAQ answer
    currentFaqEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Close FAQ answer display
 */
function closeFaqAnswer() {
    currentFaqEl.style.display = 'none';
}

/**
 * Audio event handlers
 */
function onAudioPlay() {
    statusIndicator.style.display = 'flex';
    statusText.textContent = 'Speaking...';
}

function onAudioEnded() {
    statusIndicator.style.display = 'none';
    
    // Show FAQs after topic audio ends
    if (currentTopic && faqSectionEl.style.display === 'none') {
        faqSectionEl.style.display = 'block';
    }
}

function onAudioPause() {
    if (voiceAudio.ended) {
        return; // Already handled by onAudioEnded
    }
    statusIndicator.style.display = 'none';
}

/**
 * Utility functions
 */
function showLoading(show = true) {
    // Add visual loading feedback
    if (show) {
        document.body.style.cursor = 'wait';
    } else {
        document.body.style.cursor = 'default';
    }
}

function highlightActiveTopic(topicId) {
    // Remove active class from all topics
    const allButtons = topicListEl.querySelectorAll('.topic-button');
    allButtons.forEach(btn => btn.classList.remove('active'));
    
    // Add active class to selected topic
    const activeButton = topicListEl.querySelector(`[data-topic-id="${topicId}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
}

function showError(message) {
    // Better error display than alert
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-toast';
    errorDiv.textContent = message;
    document.body.appendChild(errorDiv);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        errorDiv.classList.add('fade-out');
        setTimeout(() => errorDiv.remove(), 300);
    }, 3000);
}

function onAudioError(e) {
    console.error('Audio error:', e);
    if (audioError) {
        audioError.style.display = 'block';
    }
}

function onAudioLoaded() {
    if (audioError) {
        audioError.style.display = 'none';
    }
}

function getLanguageLabel(languageCode) {
    const labels = {
        'en': 'EN',
        'hi': 'हिं',
        'mixed': 'EN/हिं'
    };
    return labels[languageCode] || languageCode.toUpperCase();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
