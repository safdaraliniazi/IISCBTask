import React, { useState } from "react";
import axios from "axios";
import Navbar from "./Navbar";

function FileUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [inputImage, setInputImage] = useState("");
  const [outputImage, setOutputImage] = useState("");
  const [loading, setLoading] = useState(false); // State to track loading status

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setInputImage(URL.createObjectURL(event.target.files[0])); // Set input image preview
  };

  const handleUpload = async () => {
    if (selectedFile) {
      const formData = new FormData();
      formData.append("file", selectedFile);
      setLoading(true); // Set loading to true when upload starts

      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/upload",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
            responseType: "arraybuffer", // Set responseType to 'arraybuffer' to handle binary responses
          }
        );
        console.log("Success Response:", response);
        setUploadStatus("Upload successful");

        // Convert the binary data to a blob
        const blob = new Blob([response.data], { type: "image/png" });

        // Create a data URL from the blob
        const dataUrl = URL.createObjectURL(blob);

        // Set the data URL as the source for the output image
        setOutputImage(dataUrl);
      } catch (error) {
        console.error("Error:", error);
        setUploadStatus("Upload failed: " + error.message);
      } finally {
        setLoading(false); // Set loading to false when upload finishes
      }
    } else {
      setUploadStatus("No file selected");
    }
  };

  return (
    <div>
      <Navbar />

      <div className="container mt-4">
        <div className="row">
          <div className="col-md-6 mb-4">
            <h3>Select Your Image</h3>
            {inputImage && (
              <img src={inputImage} alt="Input" className="img-fluid" />
            )}
            <div className="input-group mt-3">
              <input
                type="file"
                className="form-control"
                id="inputGroupFile"
                aria-describedby="inputGroupFileAddon"
                onChange={handleFileChange}
              />
              <label className="input-group-text" htmlFor="inputGroupFile">
                Choose file
              </label>
            </div>

            <button className="btn btn-primary mt-3" onClick={handleUpload}>
              Upload
            </button>
            {uploadStatus && <p>{uploadStatus}</p>}
          </div>
          <div className="col-md-6">
            <h3>Output Image</h3>
            {/* Show loading animation if loading */}
            {loading ? (
              <div className="spinner-border" role="status">
                <span className="sr-only">Loading...</span>
              </div>
            ) : (
              // Show output image if available
              outputImage && (
                <img src={outputImage} alt="Output" className="img-fluid" />
              )
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default FileUploader;
