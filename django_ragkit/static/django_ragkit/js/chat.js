document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    const chatForm = document.getElementById("chatForm");
    const chatInput = document.getElementById("chatInput");
    const sendBtn = document.getElementById("sendBtn");
    const chatHistory = document.getElementById("chatHistory");
    const messageList = document.getElementById("messageList");
    const emptyState = document.getElementById("emptyState");
    const typingIndicator = document.getElementById("typingIndicator");
    const clearChatBtn = document.getElementById("clearChatBtn");
    let chatUuid = chatForm.dataset.chatUuid || null;
    if (!chatForm || !chatInput || !chatHistory || !messageList) {
        return;
    }


    const TYPING_DELAY_MS = 900;

    // Helpers

    function getFormattedTime() {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, "0");
        const minutes = String(now.getMinutes()).padStart(2, "0");
        return hours + ":" + minutes;
    }

    function hideEmptyState() {
        if (emptyState) {
            emptyState.classList.add("is-hidden");
        }
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    /**
     * Builds and appends a message bubble to the message list using
     * plain DOM APIs (createElement/textContent), which avoids any
     * dependency on <template> support or innerHTML parsing.
     * @param {"user"|"bot"} sender
     * @param {string} text
     */
    function appendMessage(sender, text) {
        hideEmptyState();

        const isUser = sender === "user";

        const item = document.createElement("li");
        item.className = "message-item d-flex " + (isUser ? "message-user" : "message-bot");

        const avatar = document.createElement("span");
        avatar.className = "avatar " + (isUser ? "avatar-user" : "avatar-bot");
        avatar.setAttribute("aria-hidden", "true");

        const icon = document.createElement("i");
        icon.className = "bi " + (isUser ? "bi-person-fill" : "bi-robot");
        avatar.appendChild(icon);

        const content = document.createElement("div");
        content.className = "message-content";

        const bubble = document.createElement("div");
        bubble.className = "message-bubble " + (isUser ? "bubble-user" : "bubble-bot");
        bubble.textContent = text;

        const time = document.createElement("time");
        time.className = "message-time";
        time.textContent = getFormattedTime();
        time.setAttribute("datetime", new Date().toISOString());

        content.appendChild(bubble);
        content.appendChild(time);

        item.appendChild(avatar);
        item.appendChild(content);

        messageList.appendChild(item);
        scrollToBottom();
    }

    function showTypingIndicator() {
        if (!typingIndicator) return;
        typingIndicator.classList.remove("d-none");
        typingIndicator.classList.add("d-flex");
        scrollToBottom();
    }

    function hideTypingIndicator() {
        if (!typingIndicator) return;
        typingIndicator.classList.add("d-none");
        typingIndicator.classList.remove("d-flex");
    }


    function autoResizeTextarea() {
        chatInput.style.height = "auto";
        chatInput.style.height = chatInput.scrollHeight + "px";
    }

    function updateSendButtonState() {
        if (!sendBtn) return;
        const hasContent = chatInput.value.trim().length > 0;
        sendBtn.disabled = !hasContent;
    }

    /**
     * Reads the input, appends the user message, resets the field,
     * and triggers a simulated bot reply after a short delay.
     */

    function sendQuestion() {

        // appendMessage("user", chatInput.value);
        //
        // showTypingIndicator();
        // ai
        const message = chatInput.value.trim();

        const formData = $(chatForm).serialize();

        appendMessage("user", message);

        chatInput.value = "";
        autoResizeTextarea();
        updateSendButtonState();

        showTypingIndicator();
        // end ai
        $.ajax({
            url: `/ai/chat/${chatUuid}/handle-message`,
            type: "POST",

            data: {
                question: message,
                csrfmiddlewaretoken: document.querySelector(
                    "[name=csrfmiddlewaretoken]"
                ).value
            },
            success: function (response) {
                hideTypingIndicator();
                appendMessage("bot", response.answer);
            },

            error: function (xhr) {
                hideTypingIndicator();

                if (xhr.status === 400) {
                    appendMessage("bot", "Form is not valid.");
                } else {
                    appendMessage("bot", "Server error.");
                }

                console.error(xhr.responseText);
            }
        });

    }

    function sendMessage() {

        const message = chatInput.value.trim();

        if (!message) {
            return;
        }

        if (!chatUuid) {

            $.ajax({
                url: "/ai/chat/create/",
                type: "POST",
                data: {
                    csrfmiddlewaretoken:
                    document.querySelector(
                        "[name=csrfmiddlewaretoken]"
                    ).value
                },

                success: function (response) {

                    chatUuid = response.uuid;

                    history.replaceState(
                        {},
                        "",
                        `/ai/chat/${chatUuid}/`
                    );

                    sendQuestion();
                },
                error: function (xhr) {

                    if (xhr.status === 403) {
                        appendMessage("bot", "CSRF validation failed.");
                    } else {
                        appendMessage("bot", "Could not create chat.");
                    }

                    console.error(xhr.responseText);
                }
            });

            return;
        }
        sendQuestion();
    }


    chatForm.addEventListener("submit", function (event) {
        event.preventDefault();
        sendMessage();
    });


    function handleInputKeydown(event) {
        if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
            event.preventDefault();
            sendMessage();
        }
    }

    function handleClearChat() {
        messageList.innerHTML = "";
        hideTypingIndicator();
        if (emptyState) {
            emptyState.classList.remove("is-hidden");
        }
        chatInput.focus();
    }


    // chatForm.addEventListener("submit", handleSubmit);
    chatInput.addEventListener("keydown", handleInputKeydown);
    chatInput.addEventListener("input", function () {
        autoResizeTextarea();
        updateSendButtonState();
    });


    if (clearChatBtn) {
        clearChatBtn.addEventListener("click", handleClearChat);
    }


    updateSendButtonState();
});