import { useState, useRef } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import axios from "axios";
import "./Login.css";
import { FaUser, FaLock, FaSignInAlt, FaCamera, FaArrowLeft } from "react-icons/fa";
import logo from "../../assets/lexion_icon.png";

function Login() {
  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [modoFacial, setModoFacial] = useState(false);
  const [mensajeFacial, setMensajeFacial] = useState("");
  const videoRef = useRef(null);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // ============================================================
  // 🔹 LOGIN NORMAL
  // ============================================================
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      const response = await axios.post("http://localhost:8000/login", {
        usuario,
        password,
      });

      login({
        token: response.data.access_token,
        user: {
          id: response.data.usuario_id,
          usuario: response.data.usuario,
          nombre: response.data.nombre_completo,
          email: response.data.email,
        },
      });

      const from = location.state?.from?.pathname || "/dashboard";
      navigate(from, { replace: true });
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "❌ No se pudo iniciar sesión. Verifica tus credenciales.";
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  // ============================================================
  // 🔹 LOGIN FACIAL (Reconocimiento con cámara)
  // ============================================================
  const handleLoginFacial = async () => {
    setMensajeFacial("📸 Capturando rostro...");
    setError("");
    setIsLoading(true);

    try {
      // 1️⃣ Encender cámara
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      const video = videoRef.current;
      video.srcObject = stream;
      await video.play();

      // 2️⃣ Esperar medio segundo antes de capturar
      await new Promise((r) => setTimeout(r, 500));

      // 3️⃣ Capturar un frame
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageBlob = await new Promise((resolve) =>
        canvas.toBlob(resolve, "image/jpeg")
      );

      // 4️⃣ Enviar al backend /rostro/login
      const formData = new FormData();
      formData.append("file", imageBlob);

      const res = await axios.post("http://localhost:8000/rostro/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const data = res.data;

      // 5️⃣ Procesar respuesta
      if (data.coincide) {
        setMensajeFacial(`✅ Bienvenido ${data.nombre}`);
        login({
          token: "TOKEN_FACIAL", // aquí podrías recibir un JWT real en el futuro
          user: {
            id: data.usuario_id,
            nombre: data.nombre,
          },
        });
        setTimeout(() => navigate("/dashboard"), 2000);
      } else {
        setMensajeFacial("❌ No se encontró coincidencia facial.");
      }

      // 6️⃣ Apagar cámara
      stream.getTracks().forEach((t) => t.stop());
    } catch (err) {
      console.error("Error facial:", err);
      setMensajeFacial("⚠️ No se pudo acceder a la cámara o al servidor.");
    } finally {
      setIsLoading(false);
    }
  };

  // ============================================================
  // 🔹 INTERFAZ VISUAL
  // ============================================================
  return (
    <div className="login-container">
      <div className="login-card shadow">
        <div className="login-header">
          <img src={logo} alt="Lexion Logo" className="login-logo" />
          <h1 className="login-title">Lexion</h1>
          <p className="login-subtitle">Enter your intelligent workspace</p>
        </div>

        <div className="login-body">
          {/* 🧩 MODO LOGIN NORMAL */}
          {!modoFacial ? (
            <>
              {error && <div className="alert alert-danger text-center">{error}</div>}

              <form className="login-form" onSubmit={handleSubmit}>
                <div className="form-group mb-3">
                  <label className="form-label fw-semibold">
                    <FaUser className="me-2" /> Usuario
                  </label>
                  <input
                    type="text"
                    className="form-control"
                    value={usuario}
                    onChange={(e) => setUsuario(e.target.value)}
                    required
                    placeholder="Ingresa tu usuario"
                  />
                </div>

                <div className="form-group mb-4">
                  <label className="form-label fw-semibold">
                    <FaLock className="me-2" /> Contraseña
                  </label>
                  <input
                    type="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="Ingresa tu contraseña"
                  />
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    "Cargando..."
                  ) : (
                    <>
                      <FaSignInAlt className="me-2" /> Ingresar
                    </>
                  )}
                </button>
              </form>

              <button
                className="btn btn-outline-secondary w-100 mt-3"
                onClick={() => setModoFacial(true)}
              >
                <FaCamera className="me-2" /> Ingresar con Rostro
              </button>
            </>
          ) : (
            // 🧩 MODO LOGIN FACIAL
            <div className="text-center">
              <video
                ref={videoRef}
                className="rounded shadow mb-3"
                autoPlay
                muted
                width="250"
              />
              {mensajeFacial && <p>{mensajeFacial}</p>}

              <div className="d-flex justify-content-center gap-2 mt-3">
                <button
                  className="btn btn-success"
                  disabled={isLoading}
                  onClick={handleLoginFacial}
                >
                  {isLoading ? (
                    "Procesando..."
                  ) : (
                    <>
                      <FaCamera className="me-2" /> Capturar Rostro
                    </>
                  )}
                </button>
                <button
                  className="btn btn-outline-secondary"
                  onClick={() => setModoFacial(false)}
                >
                  <FaArrowLeft className="me-2" /> Volver
                </button>
              </div>
            </div>
          )}
        </div>

        {/* 🔹 Pie del login (solo visible en modo normal) */}
        {!modoFacial && (
          <div className="login-footer text-center mt-3">
            <p>
              ¿No tienes cuenta?{" "}
              <button
                className="btn btn-link p-0"
                style={{
                  color: "#0d6efd",
                  textDecoration: "underline",
                  background: "none",
                  border: "none",
                }}
                onClick={() => navigate("/registerfacial")}
              >
                Crear cuenta
              </button>
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Login;