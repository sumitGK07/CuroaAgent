// ============================================================
// CUROAAGENT FRONTEND
// Complete frontend JavaScript
// ============================================================


// ============================================================
// BACKEND API
// ============================================================

const API_URL = "https://curoaagent-1.onrender.com/api/chat";


// ============================================================
// ELEMENTS
// ============================================================

const messages = document.getElementById("messages");
const messageInput = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");
const attachBtn = document.getElementById("attachBtn");

const researchModes =
    document.querySelectorAll(".research-mode");

const welcome = document.getElementById("welcome");

const agentStatus =
    document.getElementById("agentStatus");

const statusText =
    document.getElementById("statusText");

const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");
const step4 = document.getElementById("step4");

const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay =
    document.getElementById("sidebarOverlay");


// ============================================================
// STATE
// ============================================================

let selectedResearchEngine = "auto";
let isSending = false;


// ============================================================
// RESEARCH MODE
// ============================================================

researchModes.forEach((button) => {

    button.addEventListener("click", () => {

        researchModes.forEach((item) => {
            item.classList.remove("active");
        });

        button.classList.add("active");

        selectedResearchEngine =
            button.dataset.engine || "auto";

        console.log(
            "Research mode:",
            selectedResearchEngine
        );
    });

});


// ============================================================
// ADD USER MESSAGE
// ============================================================

function addUserMessage(text) {

    if (!messages) return;

    const message = document.createElement("div");

    message.className =
        "message-row user-row";

    message.innerHTML = `
        <div class="message-avatar user-avatar">
            <i class="fa-solid fa-user"></i>
        </div>

        <div class="message-content">

            <div class="message-role">
                You
            </div>

            <div class="message-bubble user-message">
                ${escapeHTML(text)}
            </div>

        </div>
    `;

    messages.appendChild(message);

    scrollToBottom();
}


// ============================================================
// ADD ASSISTANT MESSAGE
// ============================================================

function addAssistantMessage(
    answer,
    research,
    sources
) {

    if (!messages) return;

    const message =
        document.createElement("div");

    message.className =
        "message-row assistant-row";


    // --------------------------------------------------------
    // Research information
    // --------------------------------------------------------

    let researchHTML = "";

    if (research) {

        researchHTML = `
            <div class="research-meta">

                <span class="research-tag">
                    <i class="fa-solid fa-magnifying-glass"></i>
                    ${escapeHTML(
                        research.type ||
                        "Medical Research"
                    )}
                </span>

                <span class="research-tag">
                    ${escapeHTML(
                        research.engine ||
                        selectedResearchEngine ||
                        "auto"
                    )}
                </span>

            </div>
        `;
    }


    // --------------------------------------------------------
    // Source cards
    // --------------------------------------------------------

    let sourcesHTML = "";

    if (
        Array.isArray(sources) &&
        sources.length > 0
    ) {

        sourcesHTML = `
            <div class="sources-container">

                <div class="sources-title">

                    <i class="fa-solid fa-book-medical"></i>

                    <span>
                        Medical Sources
                    </span>

                </div>

                <div class="source-list">

                    ${sources
                        .map(
                            (source, index) =>
                                createSourceCard(
                                    source,
                                    index
                                )
                        )
                        .join("")
                    }

                </div>

            </div>
        `;
    }


    // --------------------------------------------------------
    // Complete assistant message
    // --------------------------------------------------------

    message.innerHTML = `

        <div class="message-avatar assistant-avatar">
            <i class="fa-solid fa-heart-pulse"></i>
        </div>

        <div class="message-content">

            <div class="message-role">
                CuroaAgent
            </div>

            <div class="assistant-answer">

                ${
                    answer ||
                    `
                    <p>
                        I couldn't generate an answer.
                    </p>
                    `
                }

            </div>

            ${researchHTML}

            ${sourcesHTML}

            <div class="assistant-disclaimer">

                <i class="fa-solid fa-shield-heart"></i>

                <span>
                    CuroaAgent provides general medical
                    information and does not diagnose
                    medical conditions.
                </span>

            </div>

        </div>
    `;

    messages.appendChild(message);

    scrollToBottom();
}


// ============================================================
// SOURCE CARD
// ============================================================

function createSourceCard(source, index) {

    const title =
        source?.title ||
        "Medical source";

    const snippet =
        source?.snippet ||
        "No description available.";

    const link =
        source?.link ||
        "#";

    const sourceName =
        source?.source ||
        "Medical source";

    return `
        <a
            class="source-card"
            href="${safeURL(link)}"
            target="_blank"
            rel="noopener noreferrer"
        >

            <div class="source-number">
                ${index + 1}
            </div>

            <div class="source-content">

                <div class="source-title">
                    ${escapeHTML(title)}
                </div>

                <div class="source-snippet">
                    ${escapeHTML(snippet)}
                </div>

                <div class="source-footer">

                    <span>
                        <i class="fa-solid fa-globe"></i>
                        ${escapeHTML(sourceName)}
                    </span>

                    <i
                        class="fa-solid fa-arrow-up-right-from-square"
                    ></i>

                </div>

            </div>

        </a>
    `;
}


// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {

    if (isSending) {
        return;
    }

    if (!messageInput) {
        return;
    }

    const question =
        messageInput.value.trim();

    if (!question) {
        return;
    }

    isSending = true;


    // --------------------------------------------------------
    // Hide welcome screen
    // --------------------------------------------------------

    if (welcome) {
        welcome.style.display = "none";
    }


    // --------------------------------------------------------
    // Add user message
    // --------------------------------------------------------

    addUserMessage(question);


    // --------------------------------------------------------
    // Clear input
    // --------------------------------------------------------

    messageInput.value = "";

    autoResizeTextarea();


    // --------------------------------------------------------
    // Disable send button
    // --------------------------------------------------------

    if (sendBtn) {
        sendBtn.disabled = true;
    }


    // --------------------------------------------------------
    // Show workflow
    // --------------------------------------------------------

    showWorkflow();


    try {

        // ----------------------------------------------------
        // Step 1
        // ----------------------------------------------------

        activateStep(step1);

        if (statusText) {
            statusText.textContent =
                "Understanding your question...";
        }

        await delay(400);


        // ----------------------------------------------------
        // Step 2
        // ----------------------------------------------------

        activateStep(step2);

        if (statusText) {
            statusText.textContent =
                "Selecting medical research...";
        }

        await delay(500);


        // ----------------------------------------------------
        // Step 3
        // ----------------------------------------------------

        activateStep(step3);

        if (statusText) {
            statusText.textContent =
                "Analyzing medical information...";
        }


        // ----------------------------------------------------
        // API REQUEST
        // ----------------------------------------------------

        const response =
            await fetch(
                API_URL,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message: question,
                        engine:
                            selectedResearchEngine
                    })
                }
            );


        // ----------------------------------------------------
        // Read response
        // ----------------------------------------------------

        let data;

        try {
            data = await response.json();
        }
        catch (jsonError) {
            throw new Error(
                "The backend returned an invalid response."
            );
        }


        // ----------------------------------------------------
        // Step 4
        // ----------------------------------------------------

        activateStep(step4);

        if (statusText) {
            statusText.textContent =
                "Preparing your answer...";
        }

        await delay(500);


        // ----------------------------------------------------
        // Hide workflow
        // ----------------------------------------------------

        hideWorkflow();


        // ----------------------------------------------------
        // API ERROR
        // ----------------------------------------------------

        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );
        }


        // ----------------------------------------------------
        // SHOW REAL ANSWER
        // ----------------------------------------------------

        addAssistantMessage(
            data.answer,
            data.research,
            data.sources
        );

    }
    catch (error) {

        console.error(
            "CuroaAgent error:",
            error
        );

        hideWorkflow();

        addErrorMessage(
            error.message ||
            "Unable to connect to CuroaAgent."
        );

    }
    finally {

        isSending = false;

        if (sendBtn) {
            sendBtn.disabled = false;
        }

        if (messageInput) {
            messageInput.focus();
        }
    }
}


// ============================================================
// ERROR MESSAGE
// ============================================================

function addErrorMessage(error) {

    if (!messages) return;

    const message =
        document.createElement("div");

    message.className =
        "message-row assistant-row";

    message.innerHTML = `

        <div class="message-avatar assistant-avatar">
            <i class="fa-solid fa-heart-pulse"></i>
        </div>

        <div class="message-content">

            <div class="message-role">
                CuroaAgent
            </div>

            <div class="error-box">

                <div class="error-title">

                    <i
                        class="fa-solid fa-triangle-exclamation"
                    ></i>

                    Unable to complete research

                </div>

                <p>
                    ${escapeHTML(error)}
                </p>

                <p class="error-help">

                    Please check that the CuroaAgent
                    backend is running and try again.

                </p>

            </div>

        </div>
    `;

    messages.appendChild(message);

    scrollToBottom();
}


// ============================================================
// WORKFLOW
// ============================================================

function showWorkflow() {

    if (!agentStatus) {
        return;
    }

    agentStatus.classList.remove("hidden");

    // In case CSS uses inline display
    agentStatus.style.display = "block";

    if (statusText) {
        statusText.textContent =
            "Understanding your question...";
    }

    resetSteps();

    scrollToBottom();
}


function hideWorkflow() {

    if (!agentStatus) {
        return;
    }

    agentStatus.classList.add("hidden");

    agentStatus.style.display = "none";

    if (statusText) {
        statusText.textContent =
            "Agent Online";
    }
}


function resetSteps() {

    const steps = [
        step1,
        step2,
        step3,
        step4
    ];

    steps.forEach((step) => {

        if (!step) {
            return;
        }

        step.classList.remove("active");
        step.classList.remove("completed");

    });
}


function activateStep(step) {

    if (!step) {
        return;
    }

    const allSteps = [
        step1,
        step2,
        step3,
        step4
    ];

    const currentIndex =
        allSteps.indexOf(step);

    allSteps.forEach(
        (item, index) => {

            if (!item) {
                return;
            }

            if (index < currentIndex) {

                item.classList.remove(
                    "active"
                );

                item.classList.add(
                    "completed"
                );
            }

            else if (index === currentIndex) {

                item.classList.add(
                    "active"
                );

                item.classList.remove(
                    "completed"
                );
            }

            else {

                item.classList.remove(
                    "active"
                );

                item.classList.remove(
                    "completed"
                );
            }
        }
    );
}


// ============================================================
// NEW CHAT
// ============================================================

if (newChatBtn) {

    newChatBtn.addEventListener(
        "click",
        () => {

            if (isSending) {
                return;
            }

            if (messages) {
                messages.innerHTML = "";
            }

            if (welcome) {
                welcome.style.display = "flex";
            }

            hideWorkflow();

            if (messageInput) {
                messageInput.value = "";
                autoResizeTextarea();
                messageInput.focus();
            }

            closeSidebar();

        }
    );
}


// ============================================================
// QUICK CARDS
// ============================================================

const quickCards =
    document.querySelectorAll(".quick-card");

quickCards.forEach((card) => {

    card.addEventListener(
        "click",
        () => {

            const question =
                card.dataset.question;

            if (!question) {
                return;
            }

            if (messageInput) {

                messageInput.value =
                    question;

                autoResizeTextarea();

                sendMessage();
            }

        }
    );

});


// ============================================================
// ENTER KEY
// ============================================================

if (messageInput) {

    messageInput.addEventListener(
        "keydown",
        (event) => {

            // Enter = Send
            // Shift + Enter = New Line

            if (
                event.key === "Enter" &&
                !event.shiftKey
            ) {

                event.preventDefault();

                sendMessage();
            }

        }
    );

}


// ============================================================
// AUTO RESIZE TEXTAREA
// ============================================================

if (messageInput) {

    messageInput.addEventListener(
        "input",
        autoResizeTextarea
    );

}


function autoResizeTextarea() {

    if (!messageInput) {
        return;
    }

    messageInput.style.height = "auto";

    const maxHeight = 140;

    messageInput.style.height =
        Math.min(
            messageInput.scrollHeight,
            maxHeight
        ) + "px";
}


// ============================================================
// SEND BUTTON
// ============================================================

if (sendBtn) {

    sendBtn.addEventListener(
        "click",
        sendMessage
    );

}


// ============================================================
// ATTACH BUTTON
// ============================================================

if (attachBtn) {

    attachBtn.addEventListener(
        "click",
        () => {

            alert(
                "Image analysis will be available in a future CuroaAgent version."
            );

        }
    );

}


// ============================================================
// MOBILE MENU
// ============================================================

if (menuBtn) {

    menuBtn.addEventListener(
        "click",
        () => {

            if (!sidebar) {
                return;
            }

            sidebar.classList.toggle(
                "open"
            );

            if (sidebarOverlay) {

                sidebarOverlay.classList.toggle(
                    "show"
                );
            }

        }
    );

}


if (sidebarOverlay) {

    sidebarOverlay.addEventListener(
        "click",
        closeSidebar
    );

}


function closeSidebar() {

    if (sidebar) {

        sidebar.classList.remove(
            "open"
        );
    }

    if (sidebarOverlay) {

        sidebarOverlay.classList.remove(
            "show"
        );
    }
}


// ============================================================
// SIDEBAR HISTORY
// ============================================================

const historyItems =
    document.querySelectorAll(
        ".history-item"
    );

historyItems.forEach((item) => {

    item.addEventListener(
        "click",
        () => {

            closeSidebar();

            if (messageInput) {
                messageInput.focus();
            }

        }
    );

});


// ============================================================
// SIDEBAR RESEARCH ITEMS
// ============================================================

const researchHistoryItems =
    document.querySelectorAll(
        ".research-history-item"
    );

researchHistoryItems.forEach((item, index) => {

    item.addEventListener(
        "click",
        () => {

            const engines = [
                "google",
                "google_scholar",
                "google_news"
            ];

            const engine =
                engines[index];

            if (engine) {

                selectedResearchEngine =
                    engine;

                researchModes.forEach(
                    (button) => {

                        button.classList.toggle(
                            "active",
                            button.dataset.engine ===
                            engine
                        );

                    }
                );
            }

            closeSidebar();

            if (messageInput) {
                messageInput.focus();
            }

        }
    );

});


// ============================================================
// SCROLL
// ============================================================

function scrollToBottom() {

    setTimeout(() => {

        const chatContainer =
            document.getElementById(
                "chatContainer"
            );

        if (chatContainer) {

            chatContainer.scrollTo({
                top:
                    chatContainer.scrollHeight,
                behavior: "smooth"
            });

        }

    }, 50);
}


// ============================================================
// DELAY
// ============================================================

function delay(ms) {

    return new Promise(
        (resolve) =>
            setTimeout(
                resolve,
                ms
            )
    );

}


// ============================================================
// HTML ESCAPE
// ============================================================

function escapeHTML(text) {

    if (
        text === null ||
        text === undefined
    ) {
        return "";
    }

    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ============================================================
// SAFE URL
// ============================================================

function safeURL(url) {

    try {

        const parsed =
            new URL(
                url,
                window.location.href
            );

        // Only allow HTTP and HTTPS
        if (
            parsed.protocol !== "http:" &&
            parsed.protocol !== "https:"
        ) {
            return "#";
        }

        return parsed.href
            .replace(/"/g, "&quot;");

    }
    catch {

        return "#";

    }
}


// ============================================================
// SETTINGS
// ============================================================

const settingsOverlay =
    document.getElementById(
        "settingsOverlay"
    );

const settingsBtn =
    document.getElementById(
        "settingsBtn"
    );

const closeSettingsBtn =
    document.getElementById(
        "closeSettingsBtn"
    );

const themeSelect =
    document.getElementById(
        "themeSelect"
    );

const fontSizeSelect =
    document.getElementById(
        "fontSizeSelect"
    );

const notificationToggle =
    document.getElementById(
        "notificationToggle"
    );

const privacyBtn =
    document.getElementById(
        "privacyBtn"
    );

const privacyPanel =
    document.getElementById(
        "privacyPanel"
    );

const backFromPrivacyBtn =
    document.getElementById(
        "backFromPrivacyBtn"
    );

const clearHistoryBtn =
    document.getElementById(
        "clearHistoryBtn"
    );

const clearSettingsBtn =
    document.getElementById(
        "clearSettingsBtn"
    );


// ============================================================
// OPEN SETTINGS
// ============================================================

function openSettings() {

    if (!settingsOverlay) {
        return;
    }

    settingsOverlay.classList.add(
        "active"
    );

    if (privacyPanel) {
        privacyPanel.classList.remove(
            "active"
        );
    }

    const settingsBody =
        document.querySelector(
            ".settings-body"
        );

    if (settingsBody) {
        settingsBody.style.display =
            "block";
    }

}


// ============================================================
// CLOSE SETTINGS
// ============================================================

function closeSettings() {

    if (!settingsOverlay) {
        return;
    }

    settingsOverlay.classList.remove(
        "active"
    );

}


// ============================================================
// SETTINGS BUTTON
// ============================================================

if (settingsBtn) {

    settingsBtn.addEventListener(
        "click",
        () => {

            closeSidebar();
            openSettings();

        }
    );

}


// ============================================================
// CLOSE SETTINGS BUTTON
// ============================================================

if (closeSettingsBtn) {

    closeSettingsBtn.addEventListener(
        "click",
        closeSettings
    );

}


// ============================================================
// CLICK OUTSIDE SETTINGS
// ============================================================

if (settingsOverlay) {

    settingsOverlay.addEventListener(
        "click",
        function (event) {

            if (
                event.target ===
                settingsOverlay
            ) {
                closeSettings();
            }

        }
    );

}


// ============================================================
// ESCAPE KEY
// ============================================================

document.addEventListener(
    "keydown",
    function (event) {

        if (event.key !== "Escape") {
            return;
        }

        if (
            settingsOverlay &&
            settingsOverlay.classList.contains(
                "active"
            )
        ) {
            closeSettings();
        }

        closeSidebar();

    }
);


// ============================================================
// THEME
// ============================================================

function applyTheme(theme) {

    document.body.classList.remove(
        "dark-theme"
    );

    if (theme === "dark") {

        document.body.classList.add(
            "dark-theme"
        );

    }

    else if (theme === "system") {

        const systemDark =
            window.matchMedia(
                "(prefers-color-scheme: dark)"
            ).matches;

        if (systemDark) {

            document.body.classList.add(
                "dark-theme"
            );
        }
    }

    localStorage.setItem(
        "curoa_theme",
        theme
    );
}


if (themeSelect) {

    themeSelect.addEventListener(
        "change",
        function () {

            applyTheme(
                this.value
            );

        }
    );

}


// ============================================================
// SYSTEM THEME CHANGE
// ============================================================

const systemThemeQuery =
    window.matchMedia(
        "(prefers-color-scheme: dark)"
    );

if (systemThemeQuery.addEventListener) {

    systemThemeQuery.addEventListener(
        "change",
        function () {

            const savedTheme =
                localStorage.getItem(
                    "curoa_theme"
                );

            if (savedTheme === "system") {

                applyTheme("system");

            }

        }
    );

}


// ============================================================
// FONT SIZE
// ============================================================

function applyFontSize(size) {

    document.body.classList.remove(
        "font-small",
        "font-medium",
        "font-large"
    );

    if (
        size !== "small" &&
        size !== "medium" &&
        size !== "large"
    ) {
        size = "medium";
    }

    document.body.classList.add(
        "font-" + size
    );

    localStorage.setItem(
        "curoa_font_size",
        size
    );
}


if (fontSizeSelect) {

    fontSizeSelect.addEventListener(
        "change",
        function () {

            applyFontSize(
                this.value
            );

        }
    );

}


// ============================================================
// NOTIFICATIONS
// ============================================================

if (notificationToggle) {

    notificationToggle.addEventListener(
        "change",
        async function () {

            const enabled =
                this.checked;

            localStorage.setItem(
                "curoa_notifications",
                enabled
                    ? "enabled"
                    : "disabled"
            );

            if (
                enabled &&
                "Notification" in window
            ) {

                if (
                    Notification.permission ===
                    "default"
                ) {

                    try {

                        const permission =
                            await Notification
                                .requestPermission();

                        if (
                            permission !==
                            "granted"
                        ) {

                            this.checked = false;

                            localStorage.setItem(
                                "curoa_notifications",
                                "disabled"
                            );
                        }

                    }
                    catch (error) {

                        console.log(
                            "Notification permission error:",
                            error
                        );

                    }

                }

                else if (
                    Notification.permission ===
                    "denied"
                ) {

                    alert(
                        "Notifications are blocked in your browser. Please allow notifications from your browser settings."
                    );

                    this.checked = false;

                    localStorage.setItem(
                        "curoa_notifications",
                        "disabled"
                    );
                }
            }

        }
    );

}


// ============================================================
// PRIVACY & DATA
// ============================================================

if (privacyBtn) {

    privacyBtn.addEventListener(
        "click",
        function () {

            const settingsBody =
                document.querySelector(
                    ".settings-body"
                );

            if (settingsBody) {
                settingsBody.style.display =
                    "none";
            }

            if (privacyPanel) {
                privacyPanel.classList.add(
                    "active"
                );
            }

        }
    );

}


if (backFromPrivacyBtn) {

    backFromPrivacyBtn.addEventListener(
        "click",
        function () {

            if (privacyPanel) {

                privacyPanel.classList.remove(
                    "active"
                );

            }

            const settingsBody =
                document.querySelector(
                    ".settings-body"
                );

            if (settingsBody) {

                settingsBody.style.display =
                    "block";

            }

        }
    );

}


// ============================================================
// CLEAR CHAT HISTORY
// ============================================================

if (clearHistoryBtn) {

    clearHistoryBtn.addEventListener(
        "click",
        function () {

            const confirmed =
                confirm(
                    "Are you sure you want to clear your saved chat history?"
                );

            if (!confirmed) {
                return;
            }


            // Remove known local storage keys
            localStorage.removeItem(
                "curoa_chat_history"
            );

            localStorage.removeItem(
                "chatHistory"
            );

            localStorage.removeItem(
                "curoa_history"
            );


            // Clear current visible chat
            if (messages) {
                messages.innerHTML = "";
            }

            if (welcome) {
                welcome.style.display =
                    "flex";
            }

            hideWorkflow();

            alert(
                "Your local chat history has been cleared."
            );

        }
    );

}


// ============================================================
// RESET SETTINGS
// ============================================================

if (clearSettingsBtn) {

    clearSettingsBtn.addEventListener(
        "click",
        function () {

            const confirmed =
                confirm(
                    "Reset all CuroaAgent settings to their defaults?"
                );

            if (!confirmed) {
                return;
            }

            localStorage.removeItem(
                "curoa_theme"
            );

            localStorage.removeItem(
                "curoa_font_size"
            );

            localStorage.removeItem(
                "curoa_notifications"
            );


            // Defaults
            applyTheme("light");
            applyFontSize("medium");


            if (themeSelect) {
                themeSelect.value =
                    "light";
            }

            if (fontSizeSelect) {
                fontSizeSelect.value =
                    "medium";
            }

            if (notificationToggle) {
                notificationToggle.checked =
                    false;
            }

            alert(
                "CuroaAgent settings have been reset."
            );

        }
    );

}


// ============================================================
// LOAD SAVED SETTINGS
// ============================================================

function loadCuroaSettings() {

    const savedTheme =
        localStorage.getItem(
            "curoa_theme"
        ) || "light";

    const savedFontSize =
        localStorage.getItem(
            "curoa_font_size"
        ) || "medium";

    const savedNotifications =
        localStorage.getItem(
            "curoa_notifications"
        ) === "enabled";


    // Theme
    applyTheme(savedTheme);

    if (themeSelect) {
        themeSelect.value =
            savedTheme;
    }


    // Font
    applyFontSize(savedFontSize);

    if (fontSizeSelect) {
        fontSizeSelect.value =
            savedFontSize;
    }


    // Notifications
    if (notificationToggle) {

        notificationToggle.checked =
            savedNotifications;

    }

}


// ============================================================
// ABOUT BUTTON
// ============================================================

const aboutBtn =
    document.getElementById(
        "aboutBtn"
    );

if (aboutBtn) {

    aboutBtn.addEventListener(
        "click",
        () => {

            alert(
                "CuroaAgent\n\nAI Digital Doctor for medical information and research.\n\nCuroaAgent provides educational medical information and does not replace professional medical advice."
            );

            closeSidebar();

        }
    );

}


// ============================================================
// PRIVACY & SAFETY BUTTON
// ============================================================

const privacySafetyBtn =
    document.getElementById(
        "privacySafetyBtn"
    );

if (privacySafetyBtn) {

    privacySafetyBtn.addEventListener(
        "click",
        () => {

            openSettings();

            setTimeout(() => {

                if (privacyBtn) {
                    privacyBtn.click();
                }

            }, 50);

            closeSidebar();

        }
    );

}


// ============================================================
// INITIAL STATE
// ============================================================

hideWorkflow();

loadCuroaSettings();

if (messageInput) {

    messageInput.focus();

    autoResizeTextarea();

}


// Make sure Auto is selected initially
researchModes.forEach(
    (button) => {

        button.classList.toggle(
            "active",
            button.dataset.engine === "auto"
        );

    }
);


console.log(
    "CuroaAgent frontend loaded."
);

console.log(
    "Research engine:",
    selectedResearchEngine
);
