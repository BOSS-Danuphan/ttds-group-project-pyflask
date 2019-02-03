import React, {Component} from 'react';
import './App.css';
import HomePage from './HomePage';
import SearchPage from './SearchPage';
import AboutPage from './AboutUs';
import HelpPage from './Help';
import ContactPage from './Contact';
import logo from './search-2.svg';
import {BrowserRouter as Router, Route, Link} from "react-router-dom";

class App extends Component {

    render() {
        return (
            <Router>
                <div className="App-wrapper">
                    <nav>
                        <header>
                            <img src={logo} alt="logo"/>
                            <h2>Real-Time Image Content Search</h2>
                        </header>
                        <ul>
                            <li>
                                <Link to="/">Home</Link>
                            </li>
                            <li>
                                <Link to="/about/">About</Link>
                            </li>
                            <li>
                                <Link to="/help/">Help</Link>
                            </li>
                        </ul>
                    </nav>
                    <Route path="/" exact component={HomePage}/>
                    <Route path="/search/:query?" component={SearchPage}/>
                    <Route path="/about/" component={AboutPage}/>
                    <Route path="/help/" component={HelpPage}/>
                    <Route path="/contact/" component={ContactPage}/>
                    <footer>
                        <div className="App-footer-copy">© 2019 TTDS G2. All Rights Reserved.</div>
                        <div className="App-footer-contact"><Link to='/contact/' >Contact Us</Link></div>
                    </footer>
                </div>
            </Router>
        );
    }
}

export default App;
