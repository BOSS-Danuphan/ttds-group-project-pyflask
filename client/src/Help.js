import React, {Component} from 'react';
import './Help.css';

class HelpPage extends Component {

    render() {
        return (
            <div className="HelpPage">
                <div className="Panel">
                    <h3>Help</h3>
                    <div className="Help-sketch">
                        <div className="Help-sketch-top"></div>
                        <div className="Help-sketch-bottom">
                            <div className="Help-sketch-left"></div><div className="Help-sketch-right"></div>
                        </div>
                    </div>
                    <p>The main search interface is built from 3 parts. The <b className="green">top part</b> contains
                        the search bar and inputs for adjusting search parameters. The <b className="red">left panel</b> contains
                        search results for a given query in the form of tweets. The <b className="blue">right panel</b> contains
                        a stack of real-time tweets identified as relevant to the query.
                        If "Real-time polling" found in the <b className="green">top part</b> is switched on, the <b className="blue">right panel</b> will be
                        updated with new tweets.
                    </p>
                </div>
            </div>
        );
    }
}

export default HelpPage;
