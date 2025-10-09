// firebase.js (module)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyAQ8uyD57_zgJqGr2mU14eXTWc9m0nVpNs",
  authDomain: "meu-crud-74021.firebaseapp.com",
  projectId: "meu-crud-74021",
  storageBucket: "meu-crud-74021.firebasestorage.app",
  messagingSenderId: "213475628451",
  appId: "1:213475628451:web:48894221cc482092957616",
  measurementId: "G-E5BKG501F9"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth, db };