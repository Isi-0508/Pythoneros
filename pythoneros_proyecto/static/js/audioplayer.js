document.addEventListener('DOMContentLoaded', () =>
{

const Audio = document.getElementById('audioplayer');
const PlayButton = document.getElementById('audio_toggle_play_button');
const ChangeTrackButton = document.getElementById('audio_change_track_button');
const VolumeSlider = document.getElementById('audio_volume_slider');

// REPRODUCTOR DE AUDIO
// Pausar / Reproducir

function f_play_pause_audio()
{
    if (Audio.paused)
    {
        Audio.play()
    }
    else
    {
        Audio.pause()
    }
}


// Cambiar musica (PENDIENTE)

function f_change_track_audio()
{

}

// Volumen

function f_volume_slider_audio()
{
    Audio.volume = VolumeSlider.value
}

//CONECTAR BOTONES
PlayButton.addEventListener('click', f_play_pause_audio); //Nombre de constante.addEventListener('click', nombre de funcion)
VolumeSlider.addEventListener('input', f_volume_slider_audio);
ChangeTrackButton.addEventListener('click', f_change_track_audio);
});