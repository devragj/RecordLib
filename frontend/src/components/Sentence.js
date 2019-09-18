import React from "react";
import PropTypes from 'prop-types';

function Sentence(props) {
    const sentenceStyle = {display: 'grid', gridTemplateColumns: '200px 270px 270px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '760px'};
    const { sentence_id, sentence_date, sentence_type, sentence_period, sentence_length } = props
    return (
        <div className="sentence" id={sentence_id} style={sentenceStyle}>
            <div>Date: {sentence_date}</div>
            <div>Type: {sentence_type}</div>
            <div></div>
            <div>Period: {sentence_period}</div>
            <div>Min Time: {sentence_length.min_time}</div>
            <div>Max Time: {sentence_length.max_time}</div>
        </div>
    );
}

Sentence.propTypes = {
    sentence_id: PropTypes.string,
    sentence_date: PropTypes.string,
    sentence_type: PropTypes.string,
    sentence_period: PropTypes.string,
    sentence_length: PropTypes.shape({
        min_time: PropTypes.number,
        max_time: PropTypes.number
    })
}

export default Sentence;