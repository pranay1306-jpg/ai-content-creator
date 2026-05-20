document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('content-form');
    const inputSection = document.getElementById('input-section');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');
    
    const generateBtn = document.getElementById('generate-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    
    const resetBtn = document.getElementById('reset-btn');
    
    const steps = [
        document.getElementById('step-plan'),
        document.getElementById('step-draft'),
        document.getElementById('step-opt')
    ];

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            niche: document.getElementById('niche').value,
            audience: document.getElementById('audience').value,
            platform: document.getElementById('platform').value,
            goals: document.getElementById('goals').value
        };

        // UI State: Loading
        btnText.textContent = 'Generating...';
        spinner.classList.remove('hidden');
        generateBtn.disabled = true;
        
        inputSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        
        // Fake step progression for visual feedback since backend runs synchronously
        let currentStep = 0;
        const stepInterval = setInterval(() => {
            if (currentStep < 2) {
                steps[currentStep].classList.remove('active');
                currentStep++;
                steps[currentStep].classList.add('active');
            }
        }, 4000);

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();
            clearInterval(stepInterval);
            displayResults(data);

        } catch (error) {
            clearInterval(stepInterval);
            alert(`Error generating content: ${error.message}\nMake sure your Gemini API Key is set in the server environment!`);
            resetUI();
        }
    });

    function displayResults(data) {
        loadingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        document.getElementById('res-title').textContent = data.idea_title;
        document.getElementById('res-desc').textContent = data.idea_description;
        document.getElementById('res-script').textContent = data.script;
        document.getElementById('res-caption').textContent = data.caption;
        
        const hooksList = document.getElementById('res-hooks');
        hooksList.innerHTML = '';
        data.hooks.forEach(hook => {
            const li = document.createElement('li');
            li.textContent = hook;
            hooksList.appendChild(li);
        });

        const seoContainer = document.getElementById('res-seo');
        seoContainer.innerHTML = '';
        data.seo_keywords.forEach(keyword => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.textContent = keyword;
            seoContainer.appendChild(span);
        });

        const hashtagContainer = document.getElementById('res-hashtags');
        hashtagContainer.innerHTML = '';
        data.hashtags.forEach(tag => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.textContent = tag;
            hashtagContainer.appendChild(span);
        });
    }

    function resetUI() {
        btnText.textContent = 'Generate Content ✨';
        spinner.classList.add('hidden');
        generateBtn.disabled = false;
        
        loadingSection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
        
        steps.forEach(s => s.classList.remove('active'));
        steps[0].classList.add('active');
    }

    resetBtn.addEventListener('click', resetUI);
});
