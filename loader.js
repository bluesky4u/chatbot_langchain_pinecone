function loadStylesheet(url) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.type = "text/css";
    link.href = url;
    document.head.appendChild(link);
  }
  
  function createChatbotWindow() {
    const chatbotWindow = document.createElement("div");
    chatbotWindow.id = "chatbot-window";
    document.body.appendChild(chatbotWindow);
    return chatbotWindow;
}

function playAudio(audioUrl) {
  const audio = new Audio(audioUrl);
  audio.play();
}

  

  loadStylesheet("https://thedevs.pythonanywhere.com/static/style.css");
  const chatbotWindow = createChatbotWindow();
  // chatbotWindow.style.display = "none"; // This line is not needed, as the chatbotWindow already has display set to "none" when created by the createChatbotWindow function.
  fetch("https://thedevs.pythonanywhere.com/app")
  .then((response) => response.text())
  .then((content) => {
    chatbotWindow.innerHTML = content;
    const chatBox = document.querySelector(".chatbox__support");
    const openButton = document.querySelector(".chatbox__button");
    const sendButton = document.querySelector(".send__button");
    // ...

    // Append the button to the body of the document
    document.body.appendChild(openButton);

    initChatbot(chatBox, openButton, sendButton);
  })
  .catch((error) => {
    console.error("Error fetching chatbot content:", error);
  });
  

  const scriptTag = document.getElementById('chatbotembed');
  const agent = scriptTag.getAttribute('agent');


  function initChatbot(chatBox, openButton, sendButton) {
    class Chatbox {
      constructor(chatBox, openButton, sendButton) {
        this.args = {
          openButton: openButton,
          chatBox: chatBox,
          sendButton: sendButton,
        };
        this.state = false;
        //this.messages = [];
        this.messages = [{ name: "Sam", message: "Hello, how can I help you?" }]; // Initialize an empty array to store messages

      }
  
      display() {
        const { openButton, chatBox, sendButton } = this.args;
        openButton.addEventListener("click", () => this.toggleState(chatBox));
        sendButton.addEventListener("click", () => this.onSendButton(chatBox));
  
        const node = chatBox.querySelector("input");
        node.addEventListener("keyup", ({ key }) => {
          if (key === "Enter") {
            this.onSendButton(chatBox);
          }
        });
      }
  

      
      toggleState(chatbox) {
      
        this.state = !this.state;
        if (this.state) {
          //#open
          //play sound
          //playAudio("https://files.catbox.moe/n8hwux.mp3");
          chatbox.classList.add("chatbox--active");
          chatbotWindow.style.display = "block"; // Make sure the chatbotWindow is visible when the chatbox is active
          chatbotWindow.style.position = "fixed";
          chatbotWindow.style.bottom = "60px";
          chatbotWindow.style.right = "30px";
        } else {
          //#close// (// not needed.  at the end its not needed.  you don't need that <---)
          chatbox.classList.remove("chatbox--active");
          chatbotWindow.style.display = "none"; // Hide the chatbotWindow when the chatbox is closed
        }
      }
      
      

      onSendButton(chatbox) {
        var textField = chatbox.querySelector("input");
        let text1 = textField.value;
        if (text1 === "") {
          return;
        }
        textField.value =""; //empty it
        let msg1 = { name: "User", message: text1 };
        this.messages.push(msg1);


        fetch("https://thedevs.pythonanywhere.com/predict", {
          method: "POST",
          body: JSON.stringify({ message: text1, agent: agent }),
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((r) => r.json())
          .then((r) => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
  
            this.updateChatText(chatbox);
            textField.value = "";
          })
          .catch((error) => {
            console.error("Error:", error);
  
            this.updateChatText(chatbox);
            textField.value = "";
          });
      }
  
      updateChatText(chatbox) {
        var html = "";
        this.messages
          .slice()
          .reverse()
          .forEach(function (item, index) {
            if (item.name === "Sam") {
              html +=
                '<div class="messages__item messages__item--visitor">' +
                item.message +
                "</div>";
            } else {
              html +=
                '<div class="messages__item messages__item--operator">' +
                item.message +
                "</div>";
            }
          });

      const chatmessage = chatbox.querySelector(".chatbox__messages");
      chatmessage.innerHTML = html;
      //const myDiv = document.getElementById('chatbot__support');
      chatmessage.scrollTop = chatmessage.scrollHeight;
    }
  }


  const chatbox = new Chatbox(chatBox, openButton, sendButton);
  chatbox.display();
  //chatbox.classList.remove("chatbox--active");
  chatbotWindow.style.display = "none";
  
  
  

}