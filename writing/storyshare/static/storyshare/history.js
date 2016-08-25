class PagedList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {content: [], loading: false, noMore: true, netError: false, page: 0};
    }

    componentDidMount() {
        this.getPage(0);
    }

    getPage(page) {
        this.setState({ loading: true });
        const request  = new XMLHttpRequest();

        request.onreadystatechange = () => {
            if (request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 200) {
                    const result = JSON.parse(request.responseText);
                    this.setState({
                        content: result.content,
                        loading: false,
                        noMore: result.noMore,
                        netError: false,
                        page: page,
                    });
                } else {
                    this.setState({loading: false, netError: true});
                }
            }
        };

        request.open('GET', this.getUrl + page);
        request.send();
    }

    render() {
        const page = this.state.page;

        var loadingText = '';
        if (this.state.loading) {
            loadingText = 'loading...';
        }

        if (this.state.netError) {
            return (
                    <div id="historycontainer">
                        <div id='loadingmessage'>{loadingText}</div>
                        <p>Sorry, we had a problem connecting to the server.</p>
                        <button onClick={()=>this.getPage(page)}>Try Again</button>
                    </div>
                   );
        }

        return (
                <div id="historycontainer">
                    <button onClick={()=>this.getPage(page - 1)} disabled={page <= 0}>Later</button>
                    <button onClick={()=>this.getPage(page + 1)} disabled={this.state.noMore}>Earlier</button>
                    <div id='loadingmessage'>{loadingText}</div>
                    {this.renderContent()}
                </div>
            );
    }
}

class DailyHistory extends PagedList {
    constructor(props) {
        super(props);
        this.getUrl = 'dailyhistory/';
    }

    renderContent() {
        return (<DayList days={this.state.content} />)
    }
}

class DayList extends React.Component {
    render() {
        const days = this.props.days.map(d => {
            var outcome;
            var spanClass;
            if (d.success) {
                spanClass = 'metgoal';
                outcome = '✔';
            } else if (d.today) {
                spanClass = 'ongoinggoal';
                outcome = '―';
            } else {
                spanClass = 'failedgoal';
                outcome = '✗';
            }

            return (
                    <li key={d.date}>
                        <span className='date'>{d.date}</span>
                        <span className={spanClass}>{outcome}</span>
                    </li>
                );
        });

        return (<ol>{days}</ol>);
    }
}

class PastWritings extends PagedList {
    constructor(props) {
        super(props);
        this.getUrl = 'pastwritings/';
    }

    renderContent() {
        return (<WritingList writings={this.state.content} />)
    }
}

class WritingList extends React.Component {
    render() {
        const writings = this.props.writings.map(w => {
            return (
                    <li key={w.urlId}>
                        <a href={'viewwriting/' + w.urlId}>
                            {w.title} • {w.time}
                        </a>
                    </li>
                   );
        });

        return (<ol>{writings}</ol>);
    }
}

const wl = document.getElementById('writinglist');
if (wl) {
    ReactDOM.render(
        <PastWritings />,
        wl
    );
}

const dl = document.getElementById('daylist');
if (dl) {
    ReactDOM.render(
            <DailyHistory />,
            dl
    );
}
