import axios from 'axios';
import React, { Component } from 'react';
import './App.css';



class App extends Component{
  state = {
    selectedFile: null,
    fileUploadedSuccessfully: false
  }
  onFileChange = event => {
    this.setState({selectedFile : event.target.files[0]});
  }

  

  onFileUpload = () => {
    if (!this.state.selectedFile) {
      // 파일이 선택되지 않은 경우 처리
      console.error('파일이 선택되지 않았습니다.');
      return;
    }
  
    const formData = new FormData();
    formData.append("uploadedFile", this.state.selectedFile, this.state.selectedFile.name);
  
    const config = {
      headers: {
        'Content-Type': this.state.selectedFile.type, // 이미지 파일의 Content-Type 설정
      }
    };
  
    axios.post("https://r4ji6vunwa.execute-api.ap-northeast-2.amazonaws.com/prod/file-upload", formData, config)
      .then(() => {
        this.setState({
          selectedFile: null,
          fileUploadedSuccessfully: true
        });
        // 파일 업로드 성공 시 파일 이름을 상태에 저장
        this.setState({ uploadedFileName: this.state.selectedFile.name });
      })
      .catch(error => {
        console.error('파일 업로드 오류:', error);
      });
  }
  

  fileData = () => {
    if (this.state.selectedFile){
      return(
      <div>
        <h2>파일 세부정보</h2>
        <p>파일명: {this.state.selectedFile.name}</p>
        <p>파일유형: {this.state.selectedFile.type}</p>
        <p>Last Modified: {" "}
          {this.state.selectedFile.lastModifiedDate.toDateString()}
        </p>
      </div>
      )
    } else if (this.state.fileUploadedSuccessfully){
      return(
      <div>
        <br />
        <h4>파일 정상 업로드!</h4>
      </div>
      )
    } else{
      return(
      <div>
        <br/>
        <h4> 파일을 선택하고 업로드 버튼을 클릭해 주세요.</h4>
      </div>
      )
    }
  }



  render(){
    return (
      <div className='container'>
        <div className='header'>
          <div className='head'>
            <p class="white"> Driver's license 판별 시스템</p></div></div>
            <div class="jb-division-line"></div>
          <div className='explain'>
            <details>
              <summary>👉details👈</summary>
              <p>위 사이트는 카쉐어링 서비스 중 발생할 수 있는 운전사고에 대처하기 위해 AI 영상 인식 기술을 활용하여 
              </p>운전자 얼굴 식별 및 확인 서비스 개발을 위해 이미지를 업로드 하는 사이트 입니다.
            </details>
          </div>
        <div className='content'>
        <p class="middle">License Upload</p>
        <div className='box'>
            <div className='uploader'>
              <br></br>
              <div class="filebox">
              <input class="upload-name" type="jpg" value={this.state.uploadedFileName !== null ? this.state.uploadedFileName : ''} placeholder="면허증" />
                <label for="file">파일찾기</label>
                <input type="file" onChange = {this.onFileChange} id="file"/>
                <button onClick={this.onFileUpload}>파일업로드</button>
              </div>
            </div>
            <div className='detail'>
              {this.fileData()}</div>
        </div>
        <p class="middle">Photo Upload</p>
        <div className='box'>
            <div className='uploader'>
              <br></br>
              <div class="filebox">
                <input class="upload-name" type="jpg" value={this.state.uploadedFileName || '운전자사진'} placeholder="운전자사진" />
                <label for="file">파일찾기</label>
                <input type="file" onChange = {this.onFileChange} id="file"/>
                <button onClick={this.onFileUpload}>파일업로드</button>
              </div>
            </div>
            <div className='detail'>
              {this.fileData()}</div>
        </div>
        </div>
        <div class ="copyright">Copyright ⓒ 소윤, 민경 </div>
      </div>
    )
  }
}
export default App;