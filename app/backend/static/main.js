const upload_form = document.querySelector("#upload_form");
const image_file_input = document.querySelector("#image_file");
const preview_card = document.querySelector("#preview_card");
const image_preview = document.querySelector("#image_preview");
const caption_text = document.querySelector("#caption_text");
const error_message = document.querySelector("#error_message");
const loader = document.querySelector("#loader");
const generate_button = document.querySelector("#generate_button");
const speak_button = document.querySelector("#speak_button");
const audio_player = document.querySelector("#audio_player");

const allowed_types = new Set(["image/jpeg", "image/png"]);
let current_caption = "";
let current_audio_url = null;
let current_preview_url = null;

function set_loading(is_loading) {
    loader.hidden = !is_loading;
    generate_button.disabled = is_loading;
    image_file_input.disabled = is_loading;
}

function set_error(message) {
    error_message.textContent = message;
    error_message.hidden = false;
}

function clear_error() {
    error_message.hidden = true;
    error_message.textContent = "";
}

function reset_audio() {
    if (current_audio_url !== null) {
        URL.revokeObjectURL(current_audio_url);
        current_audio_url = null;
    }

    audio_player.pause();
    audio_player.removeAttribute("src");
    audio_player.hidden = true;
}

function reset_preview() {
    if (current_preview_url !== null) {
        URL.revokeObjectURL(current_preview_url);
        current_preview_url = null;
    }

    preview_card.hidden = true;
    image_preview.removeAttribute("src");
}

function render_caption(caption) {
    current_caption = caption;
    caption_text.textContent = caption;
    speak_button.hidden = false;
    speak_button.disabled = false;
}

function clear_caption() {
    current_caption = "";
    caption_text.textContent = "Tutaj pojawi się wynik po wysłaniu obrazu.";
    speak_button.hidden = true;
    speak_button.disabled = true;
}

function validate_file(file) {
    if (!allowed_types.has(file.type)) {
        throw new Error("Backend akceptuje tylko obrazy JPG i PNG.");
    }
}

image_file_input.addEventListener("change", () => {
    reset_audio();
    clear_error();
    clear_caption();

    const selected_file = image_file_input.files[0];

    if (selected_file === undefined) {
        reset_preview();
        return;
    }

    try {
        validate_file(selected_file);
    } catch (error) {
        image_file_input.value = "";
        reset_preview();
        set_error(error.message);
        return;
    }

    reset_preview();
    current_preview_url = URL.createObjectURL(selected_file);
    preview_card.hidden = false;
    image_preview.src = current_preview_url;
});

upload_form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clear_error();
    reset_audio();
    clear_caption();

    const selected_file = image_file_input.files[0];
    if (selected_file === undefined) {
        set_error("Najpierw wybierz obraz.");
        return;
    }

    try {
        validate_file(selected_file);
        set_loading(true);

        const form_data = new FormData();
        form_data.append("file", selected_file);

        const response = await fetch("/predict", {
            method: "POST",
            body: form_data,
        });

        if (!response.ok) {
            const error_payload = await response.json();
            throw new Error(error_payload.detail);
        }

        const payload = await response.json();
        render_caption(payload.caption);
    } catch (error) {
        set_error(error.message || "Nie udalo sie wygenerowac opisu.");
    } finally {
        set_loading(false);
    }
});

speak_button.addEventListener("click", async () => {
    if (current_caption === "") {
        return;
    }

    clear_error();
    reset_audio();
    speak_button.disabled = true;

    try {
        const query = new URLSearchParams({ text: current_caption });
        const response = await fetch(`/tts?${query.toString()}`);

        if (!response.ok) {
            const error_payload = await response.json();
            throw new Error(error_payload.detail);
        }

        const audio_blob = await response.blob();
        current_audio_url = URL.createObjectURL(audio_blob);
        audio_player.src = current_audio_url;
        audio_player.hidden = false;
        await audio_player.play();
    } catch (error) {
        set_error(error.message || "Nie udalo sie odtworzyc audio.");
    } finally {
        speak_button.disabled = current_caption === "";
    }
});
