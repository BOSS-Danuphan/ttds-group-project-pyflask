import React, {Component} from 'react';
import axios from 'axios';
import './SearchPage.css';
import SearchBar from './SearchBar';
import ResultsWall from './ResultsWall';

var JSONbig = require('json-bigint');

axios.defaults.transformResponse = [function transformResponse(data) {
    /*eslint no-param-reassign:0*/
    if (typeof data === 'string') {
        try {
            data = JSONbig.parse(data);
        } catch (e) { /* Ignore */ }
    }
    return data;
}];

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            query: this.props.match.params.query || '',
            input_query: this.props.match.params.query || '',
            staticResults: [],
            rtResults: [],
            firstQuery: true,
            endpoint: process.env.REACT_APP_BACKEND_URL || window.location.origin,
            timeout: 10000,
            progress: 0,
            limit: 100,
            numberOfResults: 10,
            pollingOn: false,
            progress_timer: null,
            error: null
        };

        this.onSearchChange = this.onSearchChange.bind(this);
        this.onSearchSubmit = this.onSearchSubmit.bind(this);
        this.onNumberChange = this.onNumberChange.bind(this);
        this.onTimeoutChange = this.onTimeoutChange.bind(this);
        this.onStop = this.onStop.bind(this);
    }

    sendGetSearch(query, firstQuery = false) {
        const url = `${this.state.endpoint}/api/search?q=${query}&limit=${this.state.limit}`;
        this.props.history.push(`/search/${query}`);
        axios.get(url)
            .then(res => {
                // res.data.data = ['653229520015749121', '1092234034284056576', '1092234034284056576', '1092219188989562880', '1092218687392759809', '1092207358426664961'];
                if (res.data.data.length >= 0) {
                    const ids = [...new Set(res.data.data.map(id => id.toString()))];
                    let newState = {};
                    if (firstQuery) {
                        newState = {
                            error: null,
                            staticResults: ids,
                            firstQuery: false,
                            progress: 0
                        };
                    } else {
                        const rtTweets = this.diffResults(this.state.staticResults, this.state.rtResults, ids);
                        newState = {error: null,  rtResults: [...rtTweets, ...this.state.rtResults],progress: 0}
                    }
                    this.setState(newState)
                }
            })
            .catch(err => {
                clearInterval(this.state.progress_timer);
                this.setState({error: err, progress: 0});
                console.log('axios error', err)
            });
    }

    onSearchChange(event) {
        const query = event.target.value;
        this.setState({input_query: query});
    }

    onSearchSubmit(event) {
        clearInterval(this.state.progress_timer);
        const query = this.state.input_query;
        this.sendGetSearch(query, true);
        this.setState({
            rtResults: [],
            staticResults: [],
            query: query,
            progress_timer: this.countProgress(query),
            pollingOn: true
        });
        event.preventDefault();
    }

    onNumberChange(event){
        const number = event.target.value;
        if(number > 0) {
            this.setState({numberOfResults: event.target.value});
        }
    }

    onTimeoutChange(event){
        const timeout = event.target.value*1000,
            query = this.state.input_query;
        if (timeout > 0 ) {
            if(this.state.pollingOn){
                clearInterval(this.state.progress_timer);
                this.sendGetSearch(query);
                this.setState({
                    timeout: timeout,
                    progress_timer: this.countProgress(query, timeout)
                });
            } else {
                this.setState({timeout: timeout});
            }
        }
    }

    countProgress(query, newTimeout){
        const timeout = newTimeout || this.state.timeout;
        const refresh = 200,
            x = (100*refresh)/timeout;
        this.setState({progress: 0});
        const inner = setInterval(() => {
            if(this.state.progress >= 100){
                this.sendGetSearch(query);
                // this.setState({progress: 0});
            } else {
                const progressIncrement = this.state.progress + x;
                this.setState({progress: progressIncrement});
            }
        }, refresh);
        return inner;
    }

    onStop(event) {
        if(event){
            const query = this.state.query;
            this.sendGetSearch(query);
            this.setState({
                pollingOn: event,
                progress_timer: this.countProgress(query)
            });
        } else {
            clearInterval(this.state.progress_timer);
            this.setState({timer: null, progress_timer: null, pollingOn: event, progress: 0});
        }
    }

    isError() {
        return this.state.error != null;
    }

    isQuerySet(query) {
        return query != null && query !== '';
    }

    diffResults(staticResults, currentRtResults, newResults) {
        return newResults.filter(x => !staticResults.includes(x) && ! currentRtResults.includes(x));
    }

    componentWillMount() {
        if (this.isQuerySet(this.state.query)) {
            this.sendGetSearch(this.state.query, true);
            this.setState({
                pollingOn: true,
                progress_timer: this.countProgress(this.state.query)
            });
        }
    }

    componentWillUnmount() {
        clearInterval(this.state.timer);
        clearInterval(this.state.progress_timer)
    }

    render() {
        return (
            <div className="SearchPage">
                <SearchBar
                    query={this.state.input_query}
                    numberOfResults={this.state.numberOfResults}
                    timeout={this.state.timeout}
                    progress={this.state.progress}
                    pollingOn={this.state.pollingOn}
                    onSearchChange={this.onSearchChange}
                    onSearchSubmit={this.onSearchSubmit}
                    onNumberChange={this.onNumberChange}
                    onTimeoutChange={this.onTimeoutChange}
                    onStop={this.onStop}
                />
                {this.isError()
                    ? <p>Something went wrong.</p>
                    : <ResultsWall
                        stTweets={this.state.staticResults}
                        rtTweets={this.state.rtResults}
                        numberOfResults={this.state.numberOfResults}
                    />
                }
            </div>
        );
    }
}

export default App;
