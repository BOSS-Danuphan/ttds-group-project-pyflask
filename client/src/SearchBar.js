import React, {Component} from 'react';
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
                        <input type="text" value={this.props.query} onChange={this.handleChange} autoFocus className="SearchBar-input"/>
                        <input type="submit" value="Submit" className="SearchBar-submit"/>
                    </div>
                    <div className="SearchBar-right">
                        <input type="number" value={this.props.numberOfResults} onChange={this.handleNumberChange} className="SearchBar-number"/>
                        <input type="number" value={this.props.timeout} onChange={this.handleTimeoutChange} className="SearchBar-timeout"/>
                        <input type="button" value="Stop" onClick={this.handleStop} className="SearchBar-stop"/>
                    </div>
                </form>
            </div>
        );
    }
}

export default SearchBar;
