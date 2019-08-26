import React from "react";

function Sentence(props) {
    const sentenceStyle = {display: 'grid', gridTemplateColumns: '200px 270px 270px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '760px'};
    return (
        <div className="sentence" style={sentenceStyle}>
            <div>Date: {props.sentence_date}</div>
            <div>Type: {props.sentence_type}</div>
            <div></div>
            <div>Period: {props.sentence_period}</div>
            <div>Min Time: {props.sentence_length.min_time}</div>
            <div>Max Time: {props.sentence_length.min_time}</div>
        </div>
    );
}

export default Sentence;