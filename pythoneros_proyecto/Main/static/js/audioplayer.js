document.addEventListener('DOMContentLoaded', () => {
    const Audio = document.getElementById('audioplayer');
    const PlayButton = document.getElementById('audio_toggle_play_button');
    const VolumeSlider = document.getElementById('audio_volume_slider');
    const dropdownWhiteNoise = document.getElementById('whitenoise-dropdown');

    function f_play_pause_audio() {
        if (Audio.paused) Audio.play();
        else Audio.pause();
    }

    function f_change_track_audio(link) {
        const AudioTrack = link.dataset.track;

        Audio.innerHTML = `
            <source src="/static/sfx/${AudioTrack}.mp3" type="audio/mpeg">
            <source src="/static/sfx/${AudioTrack}.ogg" type="audio/ogg">
            <source src="/static/sfx/${AudioTrack}.wav" type="audio/wav">
            Tu navegador no soporta audio
        `;
        Audio.load();
    }

    function f_volume_slider_audio() {
        Audio.volume = VolumeSlider.value;
    }

    if (PlayButton) PlayButton.addEventListener('click', f_play_pause_audio);
    if (VolumeSlider) VolumeSlider.addEventListener('input', f_volume_slider_audio);

    // Delegación de eventos para el dropdown
    if (dropdownWhiteNoise) {
        dropdownWhiteNoise.addEventListener('click', (e) => {
            const link = e.target.closest('a'); // solo si se hace click en un <a>
            if (!link) return;
            e.preventDefault(); // evita la navegación
            f_change_track_audio(link);
        });
    }
});
