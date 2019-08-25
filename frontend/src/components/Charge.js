import React from "react";
import Sentence from "./Sentence";
import ShowHideList from "./ShowHideList";

function Charge(props) {
    const chargeStyle = {display: 'grid', gridTemplateColumns: '450px 350px', margin: '15px', border: '1px solid black', borderRadius: '10px', padding: '10px', width: '820px'};
    const sentencesRendered = props.sentences.map((sentence, index) => {
            const id = props.id + 'Case' + (index + 1).toString();
            return <Sentence {...sentence} key={id} id={id}/>;
        }
    );
    return (
        <div className="charge" id={props.id} style={chargeStyle}>
            <div>Offense: {props.offense}</div>
            <div>Grade: {props.grade}</div>
            <div>Statute: {props.statute}</div>
            <div>Disposition: {props.disposition}</div>
            {props.sentences.length > 0 &&
                <div style={{gridColumn: "1 / 3"}}>
                        <ShowHideList hidden={true} title="Sentences" list={sentencesRendered} />
                </div>
            }
        </div>
    );
}

export default Charge;