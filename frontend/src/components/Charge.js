import React from "react";
import PropTypes from 'prop-types';
import Sentence from "./Sentence";
import ShowHideList from "./ShowHideList";

function Charge(props) {
    const chargeStyle = {display: 'grid', gridTemplateColumns: '450px 350px', margin: '15px', border: '1px solid black', borderRadius: '10px', padding: '10px', width: '820px'};
    const { charge_id, offense, grade, statute, disposition, sentences } = props
    const sentencesRendered = sentences.map((sentence, index) => {
            const sentence_id = charge_id + 'Sentence' + (index + 1).toString();
            return <Sentence {...sentence} key={sentence_id} sentence_id={sentence_id}/>;
        }
    );
    return (
        <div className="charge" id={charge_id} style={chargeStyle}>
            <div>Offense: {offense}</div>
            <div>Grade: {grade}</div>
            <div>Statute: {statute}</div>
            <div>Disposition: {disposition}</div>
            {sentences.length > 0 &&
                <div style={{gridColumn: "1 / 3"}}>
                        <ShowHideList hidden={true} title="Sentences" list={sentencesRendered} />
                </div>
            }
        </div>
    );
}

Charge.propTypes = {
    charge_id: PropTypes.string,
    offense: PropTypes.string,
    grade: PropTypes.string,
    statute: PropTypes.string,
    disposition: PropTypes.string,
    sentences: PropTypes.array.isRequired
}

export default Charge;