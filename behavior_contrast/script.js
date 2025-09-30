// Configuration
const showGazeToggle = document.getElementById('showGazeToggle');
const gazeIndicator = document.getElementById('gazePositionIndicator');

// Experiment Data
let experimentData = {
    participant: '',
    settings: {
        showGaze: showGazeToggle.checked
    },
    gazeData: [],
    clicks: [],
    phases: [],
    finalScore: 0
};

// Generate random 6-digit participant ID
function generateParticipantID() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

// Initialize Webgazer
function initWebgazer() {
    return new Promise((resolve, reject) => {
        try {
            webgazer.setRegression('ridge')
                   .setGazeListener(function(data, elapsedTime) {
                       if (data) {
                           experimentData.gazeData.push({
                               x: data.x,
                               y: data.y,
                               time: elapsedTime,
                               timestamp: Date.now()
                           });
                           
                           if (showGazeToggle.checked) {
                               gazeIndicator.style.display = 'block';
                               gazeIndicator.style.left = `${data.x}px`;
                               gazeIndicator.style.top = `${data.y}px`;
                           } else {
                               gazeIndicator.style.display = 'none';
                           }
                       }
                   })
                   .begin();
            
            // Show video feed
            const video = document.querySelector('video');
            if (video) {
                document.getElementById('webgazerVideoContainer').appendChild(video);
                document.getElementById('webgazerVideoContainer').style.display = 'block';
            }
            
            setTimeout(resolve, 1000);
        } catch (error) {
            reject(error);
        }
    });
}

// Calibration function
function calibrateWebgazer() {
    return new Promise((resolve) => {
        const calibrationScreen = document.getElementById('calibration-screen');
        calibrationScreen.style.display = 'flex';
        
        const points = [
            {x: 10, y: 10},   // Top-left
            {x: 90, y: 10},   // Top-right
            {x: 10, y: 90},   // Bottom-left
            {x: 90, y: 90},   // Bottom-right
            {x: 50, y: 50}    // Center
        ];
        
        let currentPoint = 0;
        
        function showNextPoint() {
            // Clear any existing dots
            const existingDot = document.querySelector('.calibration-dot');
            if (existingDot) {
                existingDot.remove();
            }
            
            if (currentPoint >= points.length) {
                calibrationScreen.style.display = 'none';
                resolve();
                return;
            }
            
            const point = points[currentPoint];
            const dot = document.createElement('div');
            dot.className = 'calibration-dot';
            dot.style.left = `${point.x}%`;
            dot.style.top = `${point.y}%`;
            
            dot.addEventListener('click', () => {
                currentPoint++;
                setTimeout(showNextPoint, 300);
            });
            
            document.body.appendChild(dot);
        }
        
        showNextPoint();
    });
}

// [Rest of your experiment code including:
// - Experiment variables
// - Component definitions
// - Experiment functions (handleMainSquareClick, etc.)
// - Start experiment logic
// - End experiment logic
// - Data saving functions]

// Initialize participant ID when page loads
window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('participantID').value = generateParticipantID();
    
    // Start experiment when button is clicked
    document.getElementById('startExperiment').addEventListener('click', async function() {
        if (!document.getElementById('consentCheckbox').checked) {
            alert('You must consent to participate in the experiment');
            return;
        }
        
        // Record participant info
        experimentData.participant = document.getElementById('participantID').value;
        experimentData.settings.showGaze = showGazeToggle.checked;
        experimentData.gender = document.getElementById('gender').value;
        experimentData.age = document.getElementById('age').value;
        experimentData.race = document.getElementById('race').value;
        experimentData.ethnicity = document.getElementById('ethnicity').value;
        experimentData.comments = document.getElementById('comments').value;
        experimentData.consentTimestamp = new Date().toISOString();
        
        // Hide consent form
        document.getElementById('consentForm').style.display = 'none';
        
        // Show eye tracking instructions
        document.getElementById('instructions').style.display = 'block';
        document.getElementById('instructions').innerHTML = `
            <h2>Eye Tracking Setup</h2>
            <p>We'll now set up the eye tracker. Please:</p>
            <ol>
                <li>Allow camera access when prompted</li>
                <li>Keep your head still</li>
                <li>Click on each red dot as it appears</li>
            </ol>
            <button id="startCalibration">Begin Calibration</button>
        `;
        
        document.getElementById('startCalibration').addEventListener('click', async function() {
            document.getElementById('instructions').style.display = 'none';
            
            let eyeTrackingEnabled = false;
            try {
                await initWebgazer();
                await calibrateWebgazer();
                eyeTrackingEnabled = true;
            } catch (error) {
                console.error("Eye tracking setup failed:", error);
                document.getElementById('webgazerVideoContainer').style.display = 'none';
            }
            
            // Proceed with experiment
            document.getElementById('instructions').style.display = 'block';
            document.getElementById('instructions').innerHTML = `
                <h2>Main Task Instructions</h2>
                <p>Only click the big white square one time every 15 seconds.</p>
                <p>When the small square appears, click it quickly.</p>
                ${!eyeTrackingEnabled ? '<p style="color:yellow;">Note: Eye tracking is not active</p>' : ''}
                <p>Press any key to begin.</p>
            `;
            
            document.addEventListener('keydown', function startHandler() {
                document.removeEventListener('keydown', startHandler);
                document.getElementById('instructions').style.display = 'none';
                
                // Start main experiment
                document.getElementById('mainSquare').onclick = handleMainSquareClick;
                experimentStartTime = Date.now();
                startComponent();
            }, {once: true});
        });
    });
});

// Make download functions available globally
window.downloadDataAsJSON = function() {
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-');
    const dataStr = JSON.stringify(experimentData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const dataUrl = URL.createObjectURL(dataBlob);
    
    const downloadLink = document.createElement('a');
    downloadLink.href = dataUrl;
    downloadLink.download = `experiment_data_${experimentData.participant}_${timestamp}.json`;
    downloadLink.click();
};

window.downloadDataAsCSV = function() {
    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "timestamp,x,y\n";
    
    experimentData.gazeData.forEach(gaze => {
        csvContent += `${gaze.timestamp},${gaze.x},${gaze.y}\n`;
    });
    
    const encodedUri = encodeURI(csvContent);
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-');
    const downloadLink = document.createElement("a");
    downloadLink.setAttribute("href", encodedUri);
    downloadLink.setAttribute("download", `gaze_data_${experimentData.participant}_${timestamp}.csv`);
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
};

window.downloadBackupData = function() {
    const now = new Date();
    const timestamp = now.toISOString().replace(/[:.]/g, '-');
    const dataStr = JSON.stringify(experimentData, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const dataUrl = URL.createObjectURL(dataBlob);
    
    const downloadLink = document.createElement('a');
    downloadLink.href = dataUrl;
    downloadLink.download = `experiment_backup_${experimentData.participant}_${timestamp}.json`;
    downloadLink.click();
};