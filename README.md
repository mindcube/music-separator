Replace:

- `/path/to/your/audiofile.mp3` with the path to your audio file.
- `/desired/output/folder` with your target directory for saving the stems.
- `htdemucs` with your model of choice, if required.

### How It Works

1. **Argument Building:**  
   The script builds a list of command-line style arguments (including model name, device, output directory, and input file) to configure Demucs's separation process.

2. **Delegating the Separation:**  
   The main separation work is carried out by a direct call to Demucs’ CLI function (`demucs_separate_main`), which processes the input file based on the provided parameters.

3. **Stem Extraction and Saving:**  
   After processing, the separated stems are saved as WAV files using `torchaudio` patched with `soundfile` to ensure the files are correctly written.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests if you have ideas or improvements.

1. Fork the repository.
2. Create a new branch for each feature or bug fix.
3. Send a pull request describing your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Facebook Research Demucs](https://github.com/facebookresearch/demucs) for the separation framework.
- The open source community for their invaluable contributions.
