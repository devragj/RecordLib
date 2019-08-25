import React, { useState } from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPlusCircle, faMinusCircle } from '@fortawesome/free-solid-svg-icons'

function ShowHideList(props) {
        const [listHidden, setListHidden] = useState(props.hidden);

        const handlePlusClick = () => {
                setListHidden(false);
        }

        const handleMinusClick = () => {
                setListHidden(true);
        }

        const iconStyle = {marginLeft: '10px'};

        return (
            <div className="showHideList">
                <h5>{props.title}
                    { listHidden?   <FontAwesomeIcon icon={faPlusCircle} style={iconStyle} onClick={handlePlusClick}/>: <FontAwesomeIcon icon={faMinusCircle} style={iconStyle} onClick={handleMinusClick}/>
                    }

                    </h5>
                {!listHidden && props.list}
            </div>
        );
}

export default ShowHideList;