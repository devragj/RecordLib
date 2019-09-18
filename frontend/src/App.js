import React, {useState} from "react";
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import CRecordWrapper from "./components/CRecord";
import { fetchCRecord } from "./actions";

/**
 * Parent component
 *
 * The user can upload a Summary PDF file.
 * Clicking "Upload" will send the file to the backend
 * to be processed into a CRecord.
 * The returned JSON will be processed and sent to the redux store.
 * After that, this component can render a child CRecord component.
 */
function App(props) {
    const { cRecordPresent, fetchCRecord } = props;
    const [selectedFile, setSelectedFile] = useState(null);

    const onChangeHandler = event => {
        setSelectedFile(event.target.files[0]);
    }

    const onClickHandler = () => {
        fetchCRecord(selectedFile);
    };

    const uploadStyle = {
        margin: '15px',
        border: '1px solid black',
        borderRadius: '5px',
        padding: '10px',
        width: '950px'
    };

    return (<main className="content" style={{ margin: '20px'}}>
        <div className="fileUpload" style={uploadStyle}>
            <input type="file" name="file" onChange={onChangeHandler}/>
            <button type="button" onClick={onClickHandler} style={{
                            marginLeft: '20px'
                }}>Upload</button>
        </div>
            {cRecordPresent && <CRecordWrapper />}
    </main>);
};

App.propTypes = {
    cRecordPresent: PropTypes.bool,
    fetchCRecord: PropTypes.func.isRequired
};

function mapStateToProps(state) {
    return { cRecordPresent: state.entities? true: false };
};

function mapDispatchToProps(dispatch) {
    return { fetchCRecord: file => dispatch(fetchCRecord(file)) };
};

export default connect(mapStateToProps, mapDispatchToProps)(App);