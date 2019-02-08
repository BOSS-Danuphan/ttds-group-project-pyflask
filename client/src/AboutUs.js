import React, {Component} from 'react';
import './AboutUs.css';

class AboutPage extends Component {

    render() {
        return (
            <div className="AboutPage">
                <div className="Panel">
                    <h3>About</h3>
                    <p>The Real-time Image Content Search is a group project
                        developed by MSc students at The University of Edinburgh
                        for the Text Technologies for Data Science course.
                        The aim of this project was to create an IR tool for Twitter images
                        that improves on pure textsearch by incorporating information
                        from machine vision-recognition systems. </p>
                </div>
            </div>
        );
    }
}

export default AboutPage;
