  const prefix = "I am a ";
  const suffix = " tool";
  const messages = [
    "sustainability",
    "awareness",
    "messenger"
  ];

  let currentMessage = 0;
  let currentChar = 0;
  let deleting = false;

  function type() {
    const message = messages[currentMessage];
    const textElement = document.getElementById("text");
    
    if (deleting) {
      textElement.innerText = prefix + message.substring(0, currentChar - 1) + suffix;
      currentChar--;

      if (currentChar === 0) {
        deleting = false;
        currentMessage++;
        if (currentMessage >= messages.length) {
          currentMessage = 0;
        }
      }
    } else {
      textElement.innerText = prefix + message.substring(0, currentChar + 1) + suffix;
      currentChar++;

      if (currentChar === message.length) {
        deleting = true;
      }
    }

    setTimeout(type, deleting ? 50 : 200);
  }

  document.addEventListener("DOMContentLoaded", () => {
    type();
  });