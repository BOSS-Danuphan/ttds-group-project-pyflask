import React, {Component} from 'react';
import {DebounceInput} from 'react-debounce-input';
import Switch from "react-switch";
import './SearchBar.css';

class SearchBar extends Component {

    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleNumberChange = this.handleNumberChange.bind(this);
        this.handleTimeoutChange = this.handleTimeoutChange.bind(this);
        this.handleStop = this.handleStop.bind(this);
    }

    handleChange(event) {
        this.props.onSearchChange(event);
    }

    handleSubmit(event) {
        this.props.onSearchSubmit(event);
    }

    handleNumberChange(event){
        this.props.onNumberChange(event);
    }

    handleTimeoutChange(event){
        this.props.onTimeoutChange(event);
    }

    handleStop(event) {
        this.props.onStop(event);
    }

    render() {
        return (
            <div className="SearchBar">
                <form onSubmit={this.handleSubmit}>
                    <div className="SearchBar-left">
                        <input type="text" value={this.props.query} onChange={this.handleChange} placeholder="Type a query" autoFocus className="SearchBar-input"/>
                        <input type="submit" value="Submit" className="SearchBar-submit"/>
                    </div>
                    <div className="SearchBar-right">
                        <div className="SearchBar-input-pair">
                            <p>Number of results:</p>
                            <DebounceInput
                                debounceTimeout={300}
                                type="number"
                                value={this.props.numberOfResults}
                                onChange={this.handleNumberChange}
                                className="SearchBar-number"
                                min="1" max="100"
                                />
                        </div>
                        <div className="SearchBar-input-pair">
                            <p>Refresh interval:</p>
                            <DebounceInput
                                debounceTimeout={500}
                                type="number"
                                value={this.props.timeout/1000}
                                onChange={this.handleTimeoutChange}
                                className="SearchBar-timeout"
                                min="1" max="3600"
                            />
                        </div>
                        <div className="SearchBar-input-pair">
                            <p className="switch">Real-time polling:</p>
                            <Switch
                                onChange={this.handleStop}
                                checked={this.props.pollingOn}
                                id="normal-switch"
                                height={34}
                                width={70}
                            />
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}

export default SearchBar;
