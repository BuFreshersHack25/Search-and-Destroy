Webcam.set({
 constraints: {
   facingMode: 'environment'
 }
});
Webcam.attach('#cameraVideo');
var image_taken;
document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const shutterBtn = document.getElementById('shutterBtn');
    const retakeBtn = document.getElementById('retakeBtn');
    const getInfoBtn = document.getElementById('getInfoBtn');
    const canvasEl = document.getElementById('cameraVideo');
    const cameraControls = document.querySelector('.camera-controls');
    
    const resultSheet = document.getElementById('resultSheet');
    const resultImage = document.getElementById('resultImage');
    const resultTitle = document.getElementById('resultTitle');
    const resultBody = document.getElementById('resultBody');
    const dragHandle = document.querySelector('.drag-handle');

    const menuBtn = document.getElementById('menuBtn');
    const navOverlay = document.getElementById('navOverlay');
    const closeNavBtn = document.getElementById('closeNavBtn');
    
    // UI States
    const UI_STATES = { STREAMING: 'streaming', CAPTURED: 'captured', SUBMITTING: 'submitting' };
    
    const updateUI = (state) => {
      shutterBtn.classList.toggle('is-hidden', state !== UI_STATES.STREAMING);
      getInfoBtn.classList.toggle('is-hidden', state !== UI_STATES.CAPTURED);
      retakeBtn.classList.toggle('is-hidden', state !== UI_STATES.CAPTURED);
      
      cameraControls.classList.toggle('is-captured', state === UI_STATES.CAPTURED || state === UI_STATES.SUBMITTING);
      
      canvasEl.style.opacity = (state === UI_STATES.STREAMING) ? '0' : '1';
      
      getInfoBtn.disabled = retakeBtn.disabled = (state === UI_STATES.SUBMITTING);
      
      if (state === UI_STATES.SUBMITTING) {
        getInfoBtn.innerHTML = `<div class="spinner-border spinner-border-sm" role="status"></div>`;
      } else {
        getInfoBtn.innerHTML = `<i class="bi bi-check-lg"></i>`;
      }
    };

    // --- UI SIMULATION LOGIC ---
    const takePicture = () => {
      Webcam.snap( function(data_uri) {
        document.getElementById("cameraVideo").innerHTML = '<img src="'+data_uri+'"/>';
        image_taken = data_uri;
      })
      updateUI(UI_STATES.CAPTURED);
     
    }
    const retakePicture = () => {
      updateUI(UI_STATES.STREAMING);
      hideSheet();
    };
    
    const showSheet = () => {
      resultSheet.classList.add('is-visible');
    };
    
    const hideSheet = () => {
      resultSheet.classList.remove('is-visible');
    };

    const showNav = () => {
      navOverlay.classList.add('is-visible');
    }

    const hideNav = () => {
      navOverlay.classList.remove('is-visible');
    }

    // Simulate getting info
    const getSpeciesInfo = () => {
      var xhr = new XMLHttpRequest();
      xhr.open("POST", "/image", true);
      xhr.send(image_taken);
      updateUI(UI_STATES.SUBMITTING);
      //resultImage.src = "placeholder 80x80"; // Placeholder
      resultTitle.textContent = "Analyzing...";
      resultBody.innerHTML = `<div class="loader-container"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>`;
      showSheet();

      // Simulate API call delay
      setTimeout(() => {
        resultTitle.textContent = "Example Species";
        resultBody.innerHTML = `<p>This is a sample description for the identified species. It would typically explain its characteristics and habitat.</p><p>This species is considered invasive. Citizens are advised to report sightings to the local authorities and not attempt to remove it themselves.</p>`;
        updateUI(UI_STATES.CAPTURED);
      }, 1500);
    };

    // Event Listeners
    shutterBtn.addEventListener('click', takePicture);
    retakeBtn.addEventListener('click', retakePicture);
    getInfoBtn.addEventListener('click', getSpeciesInfo);
    dragHandle.addEventListener('click', hideSheet);
    menuBtn.addEventListener('click', showNav);
    closeNavBtn.addEventListener('click', hideNav);

    // Initial State
    updateUI(UI_STATES.STREAMING);
  });


