const sound = {
  65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav",
  87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav",
  83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav",
  69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav"
};

// Tracking the key sequence
const sequence = ['w', 'e', 's', 'e', 'e', 'y', 'o', 'u'];
let typedSequence = [];

// Mouseover event listener for highlighting piano keys
document.querySelectorAll('.piano-key').forEach(key => {
  key.addEventListener('mouseover', () => {
      const keyInfo = document.getElementById('key-info');
      const keyText = key.getAttribute('data-key') || key.querySelector('span').textContent;
  });
  key.addEventListener('mouseout', () => {
      const keyInfo = document.getElementById('key-info');
  });
});

// Keydown event listener for pressing keys and playing sounds
document.addEventListener('keydown', (event) => {
  const keyCode = event.keyCode;
  const key = event.key.toLowerCase();

  if (sound[keyCode]) {
      const audio = new Audio(sound[keyCode]);
      audio.play();

      let keyElement;
      if (keyCode === 186) {
          keyElement = document.querySelector('.piano-key[data-key=";"]');
      } else {
          keyElement = document.querySelector(`.piano-key[data-key="${key.toUpperCase()}"]`);
      }
      
      if (keyElement) {
          keyElement.style.transform = 'scale(0.9)'; 
          keyElement.style.boxShadow = '0 4px 8px rgba(0,0,0,0.3)';
          setTimeout(() => {
              keyElement.style.transform = ''; 
              keyElement.style.boxShadow = '';
          }, 200);
      }
  }

  typedSequence.push(key);

  if (typedSequence.length > sequence.length) {
      typedSequence.shift(); 
     }

  if (typedSequence.join('') === sequence.join('')) {
      awakenGreatOldOne();
  }
});

function awakenGreatOldOne() {
  // Remove the fade-out effect from the piano
  const piano = document.querySelector('.piano');
  piano.style.transition = 'opacity 2s ease';  
  piano.style.opacity = 0; 


  setTimeout(() => {
      piano.innerHTML = ''; 

      piano.style.opacity = 1;
      //Create a new div to hold the new content
      const newContent = document.createElement('div');
      newContent.style.position = 'relative'; 
      newContent.style.zIndex = '10';  
      newContent.style.borderRadius = '30px 30px 0px 0px';
      newContent.style.display = 'flex';
      newContent.style.alignItems = 'center';
      newContent.style.textAlign = 'center';
      newContent.style.justifyContent = 'center';



      // Replace with image of the Great Old One
      const oldOneImage = document.createElement('img');
      oldOneImage.src = '/static/piano/images/texture.jpeg'; 
      oldOneImage.style.width = '100%'; 
      oldOneImage.style.height = 'auto'; 
      oldOneImage.style.borderRadius = '30px 30px 0px 0px'; 

      //Create and append the "I have awoken" text
      const text = document.createElement('div');
      text.classList.add('old');
      text.textContent = 'I have awoken.';
      text.style.alignItems = 'center';

      // Append image and text
      newContent.appendChild(oldOneImage);
      newContent.appendChild(text);
      
      // Add to piano
      piano.appendChild(newContent);

      // Play the creepy audio
      const creepyAudio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3'); // Replace with actual audio URL
      creepyAudio.play();

  }, 2000);

  // Disable further key presses
  document.removeEventListener('keydown', arguments.callee);
}