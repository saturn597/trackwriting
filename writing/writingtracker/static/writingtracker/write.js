class WordCount extends React.Component {
    constructor(props) {
        super(props);

        this.textArea = props.textArea;

        this.state = {wordcount: this.countWords()};

        this.textArea.onkeyup = () => {
            this.setState({wordcount: this.countWords()})
        };
    }

    countWords() {
        var wordcount;
        if (this.textArea.value === '') {
            // Splitting an empty string returns an array of length 1.
            // So handle this case separately.
            wordcount = 0;
        } else {
            // Split the value by whitespace and count the resulting array
            // to find the word count. The trim() is needed since otherwise
            // trailing whitespace gets counted as a word.
            wordcount = this.textArea.value.trim().split(/\s+/).length;
        }
        return wordcount;
    };

    render() {
        return (
                <div>
                    {this.state.wordcount}
                </div>
               );
    }
}

ReactDOM.render(<WordCount textArea={document.getElementById('id_text')} />, document.getElementById('wordcount'));
