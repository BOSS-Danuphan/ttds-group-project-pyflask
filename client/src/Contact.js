import React, {Component} from 'react';
import logo from './GitHub-Mark-32px.png';
import './Contact.css';

class ContactPage extends Component {

    render() {
        return (
            <div className="ContactPage">
                <div className="Panel">
                    <h3>Contact</h3>
                    <ul>
                        <li><p>Azizah</p><a href="https://github.com/AlAzizah"><img alt="GitHub Logo" src={logo}/></a></li>
                        <li><p>Adam</p><a href="https://github.com/adamdotdev"><img alt="GitHub Logo" src={logo}/></a></li>
                        <li><p>Pavlos</p><a href="https://github.com/pgogousis"><img alt="GitHub Logo" src={logo}/></a></li>
                        <li><p>Hansun</p><a href="https://github.com/joanna350"><img alt="GitHub Logo" src={logo}/></a></li>
                        <li><p>Danuphan</p><a href="https://github.com/BOSS-Danuphan"><img alt="GitHub Logo" src={logo}/></a></li>
                        <li><p>Maciej</p><a href="https://github.com/Machkeck"><img alt="GitHub Logo" src={logo}/></a></li>
                    </ul>
                </div>
            </div>
        );
    }
}

export default ContactPage;
