import React, {useState} from "react"













function PetitionStepper(props) {
    const [selectedFile, setSelectedFile] = useState(null);

    const onChangeHandler = event => {
        setSelectedFile(event.target.files[0]);
    }

    const onClickHandler = () => {
        fetchCRecord(selectedFile);
    };

   return (
        <div>
            <h2> Upload Files </h2>
            <div className="fileUpload" style={uploadStyle}>
                <input type="file" name="file" onChange={onChangeHandler}/>
                <button type="button" onClick={onClickHandler} style={{
                    marginLeft: '20px'
                }}>Upload</button>
            </div>
            {cRecordPresent && <CRecordWrapper />}
        </div>
    )
}