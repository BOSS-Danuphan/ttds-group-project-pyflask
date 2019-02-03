import React, {Component} from 'react';
import {withRouter} from "react-router-dom";
import './HomePage.css';


class HomePage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            query: '',
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }

    handleSubmit(event) {
        event.preventDefault();
        this.props.history.push(`/search/${this.state.query}`);
    }

    handleChange(event) {
        this.setState({query: event.target.value});
    }

    render() {
        return (
            <div className="HomePage">
                <form onSubmit={this.handleSubmit}>
                    <input type="text" value={this.props.query} onChange={this.handleChange} placeholder="Type a query" className="HomePage-input" autoFocus />
                    <input type="submit" value="Search" className="HomePage-submit"/>
                </form>
            </div>
        );
    }
}

export default withRouter(HomePage);