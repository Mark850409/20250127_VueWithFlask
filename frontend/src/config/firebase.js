// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCmqa6FRrHYbFbZ_OCYW1qT4Rf6pRjr7-I",
  authDomain: "recommendsystem-3c5f1.firebaseapp.com",
  projectId: "recommendsystem-3c5f1",
  storageBucket: "recommendsystem-3c5f1.firebasestorage.app",
  messagingSenderId: "391997459196",
  appId: "1:391997459196:web:58c34e2b892681a4d66579",
  measurementId: "G-J7JJJ2YW6B"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);