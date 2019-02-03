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
            results: [],
            staticResults: [],
            rtResults: [],
            firstQuery: true,
            endpoint: process.env.REACT_APP_BACKEND_URL || window.location.origin,
            timeout: 10000,
            numberOfResults: 10,
            pollingOn: true,
            timer: null,
            error: null
        };

        this.onSearchChange = this.onSearchChange.bind(this);
        this.onSearchSubmit = this.onSearchSubmit.bind(this);
        this.onNumberChange = this.onNumberChange.bind(this);
        this.onTimeoutChange = this.onTimeoutChange.bind(this);
        this.onStop = this.onStop.bind(this);
    }

    sendGetSearch(query, firstQuery = false) {
        const url = `${this.state.endpoint}/api/search?q=${query}&limit=${this.state.numberOfResults}`;
        this.props.history.push(`/search/${query}`);
        axios.get(url)
            .then(res => {
                if (res.data.data.length >= 0) {
                    const ids = res.data.data.map(id => id.toString())
                    const rtTweets = this.diffResults(this.state.staticResults, ids);
                    const newState = {
                        error: null,
                        results: ids,
                        staticResults: ids,
                        rtResults: [...rtTweets, ...this.state.rtResults].slice(0, this.state.numberOfResults)
                    };
                    this.setState(newState)
                }
            })
            .catch(err => {
                this.setState({error: err});
                console.log('axios error', err)
            });
    }

    onSearchChange(event) {
        this.setState({input_query: event.target.value});
    }

    onSearchSubmit(event) {
        clearInterval(this.state.timer);
        const query = this.state.input_query;
        this.sendGetSearch(query, true);
        this.setState({
            results: [],
            rtResults: [],
            staticResults: [],
            query: query,
            timer: setInterval(() => this.sendGetSearch(query), this.state.timeout),
            pollingOn: true
        });
        event.preventDefault();
    }

    onNumberChange(event){
        this.setState({numberOfResults: event.target.value});
    }

    onTimeoutChange(event){
        const timeout = event.target.value*1000,
            query = this.state.input_query;
        if(this.state.pollingOn){
            clearInterval(this.state.timer);
            this.sendGetSearch(query/*, true*/);
            this.setState({
                timeout: timeout,
                timer: setInterval(() => this.sendGetSearch(query), timeout)
            });
        } else {
            this.setState({timeout: timeout});
        }

    }

    onStop(event) {
        console.log('onStop', event);
        if(event){
            const query = this.state.query;
            this.sendGetSearch(query);
            this.setState({
                timer: setInterval(() => this.sendGetSearch(query), this.state.timeout),
                pollingOn: event
            });
        } else {
            clearInterval(this.state.timer);
            this.setState({timer: null, pollingOn: event});
        }
    }

    isError() {
        return this.state.error != null;
    }

    isQuerySet(query) {
        return query != null && query !== '';
    }

    diffResults(currentResults, newResults) {
        return newResults.filter(x => !currentResults.includes(x));
    }

    componentWillMount() {
        if (this.isQuerySet(this.state.query)) {
            this.sendGetSearch(this.state.query, true);
            this.setState({
                results: [],
                timer: setInterval(() => this.sendGetSearch(this.state.query), this.state.timeout)
            });
        }
    }

    componentWillUnmount() {
        clearInterval(this.state.timer);
    }

    render() {
        return (
            <div className="SearchPage">
                <SearchBar
                    query={this.state.input_query}
                    numberOfResults={this.state.numberOfResults}
                    timeout={this.state.timeout}
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
                        tweets={this.state.results}
                        stTweets={this.state.staticResults}
                        rtTweets={this.state.rtResults}
                    />
                }
            </div>
        );
    }
}

export default App;
