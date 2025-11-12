function loginAdmin() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;

  if (user === "admin" && pass === "12345") {
    alert("Login berhasil! Selamat datang, Admin.");
    window.location.href = "/"; // nanti ganti jadi URL dashboard
    return false;
  } else {
    alert("Username atau password salah!");
    return false;
  }
}