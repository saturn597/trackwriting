class WordCount extends React.Component {
    constructor(props) {
        super(props);
        this.state = {wordcount: 0};

        const textArea = document.getElementById('id_text');
        textArea.onkeyup = () => {
            var wordcount;
            if (textArea.value === '') {
                // Splitting an empty string returns an array of length 1.
                // So handle this case separately.
                wordcount = 0;
            } else {
                // Split the value by whitespace and count the resulting array
                // to find the word count. The trim() is needed since otherwise
                // trailing whitespace gets counted as a word.
                wordcount = textArea.value.trim().split(/\s+/).length;
            }
            this.setState({wordcount: wordcount});
        };

    }

    render() {
        return (
                <div>
                    {this.state.wordcount}
                </div>
               );
    }
}

ReactDOM.render(<WordCount />, document.getElementById('wordcount'));
