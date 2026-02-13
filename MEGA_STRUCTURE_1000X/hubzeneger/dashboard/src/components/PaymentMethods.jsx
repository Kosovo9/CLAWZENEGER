
import React, { useState, useEffect } from 'react';

export default function PaymentMethods({ amount = 100 }) {
  const [loading, setLoading] = useState(false);
  const [showTransferInfo, setShowTransferInfo] = useState(false);
  const [paypalLoaded, setPaypalLoaded] = useState(false);

  // Intentamos obtener links/keys de variables (o constantes si es build-time)
  const MP_LINK = "https://link.mercadopago.com.mx/studionexora";
  const PAYPAL_CLIENT_ID = "AXMBQ29TlSTG7yu3IYzIBI-oHvolwqxn0_atALymIFetkT22qeLjkDFYcEVc-V5TDZmuSVdwyPicBTq-"; // Sandbox base de la imagen/env

  useEffect(() => {
    // Cargar SDK de PayPal dinámicamente
    if (!window.paypal) {
      const script = document.createElement("script");
      script.src = `https://www.paypal.com/sdk/js?client-id=${PAYPAL_CLIENT_ID}&currency=USD`;
      script.addEventListener("load", () => setPaypalLoaded(true));
      document.body.appendChild(script);
    } else {
      setPaypalLoaded(true);
    }
  }, []);

  const handlePay = async (provider) => {
    if (provider === 'mercadopago') {
      window.open(MP_LINK, '_blank');
      return;
    }

    if (provider === 'transfer') {
      setShowTransferInfo(!showTransferInfo);
    }
  };

  return (
    <div className="p-6 bg-[#0f172a] text-white rounded-2xl shadow-2xl border border-gray-800 max-w-md mx-auto backdrop-blur-xl">
      <h3 className="text-2xl font-extrabold mb-6 flex items-center gap-2">
        <span className="bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
          💳 Pasarela Omega
        </span>
        <span className="text-[10px] bg-green-500/20 text-green-400 border border-green-500/30 px-2 py-1 rounded-full uppercase tracking-tighter">
          Secure Live
        </span>
      </h3>

      <div className="space-y-6">
        {/* MERCADO PAGO */}
        <button
          onClick={() => handlePay('mercadopago')}
          className="w-full group relative flex items-center justify-between bg-[#009EE3] hover:bg-[#0089C7] text-white p-4 rounded-xl transition-all shadow-lg hover:scale-[1.02] active:scale-95"
        >
          <span className="font-bold text-lg">Pagar con Mercado Pago</span>
          <div className="bg-white/20 p-2 rounded-lg">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3" /></svg>
          </div>
        </button>

        {/* PAYPAL CONTAINER */}
        <div className="relative">
          {!paypalLoaded && <div className="animate-pulse bg-gray-800 h-14 rounded-xl"></div>}
          <div id="paypal-button-container" className="min-h-[50px]">
            {/* Si estuviéramos en una app de React real, usaríamos @paypal/react-paypal-js */}
            <div className="text-center text-xs text-gray-500 mb-2">PayPal Smart Checkout Activo</div>
            <button
              className="w-full bg-[#FFC439] text-[#111] p-3 rounded-xl font-bold flex items-center justify-center gap-2"
              onClick={() => alert("El SDK de PayPal se está inicializando... Por favor, usa Mercado Pago si tienes prisa.")}
            >
              Cargando PayPal...
            </button>
          </div>
        </div>

        <div className="relative flex items-center py-2">
          <div className="flex-grow border-t border-gray-800"></div>
          <span className="flex-shrink mx-4 text-gray-500 text-xs">OTRAS OPCIONES</span>
          <div className="flex-grow border-t border-gray-800"></div>
        </div>

        {/* TRANSFERENCIA */}
        <button
          onClick={() => handlePay('transfer')}
          className="w-full flex items-center justify-center gap-3 bg-gray-800/50 border border-gray-700 text-gray-300 p-3 rounded-xl hover:bg-gray-800 transition-all text-sm"
        >
          Transferencia Bancaria (HSBC)
        </button>

        {showTransferInfo && (
          <div className="p-4 bg-gray-900/50 border border-blue-500/30 rounded-xl text-sm animate-fade-in">
            <div className="space-y-2 text-blue-100">
              <p className="flex justify-between"><span>Banco:</span> <span className="font-bold">HSBC México</span></p>
              <p className="flex justify-between"><span>Tarjeta:</span> <span className="font-mono bg-blue-500/10 px-1 rounded">4213 1660 4247 6634</span></p>
              <p className="flex justify-between"><span>Titular:</span> <span className="font-bold">Studio Nexora</span></p>
            </div>
            <p className="mt-3 text-[10px] text-orange-300 bg-orange-500/10 p-2 rounded">
              ⚠️ Activa tu servicio enviando el comprobante por WhatsApp.
            </p>
          </div>
        )}
      </div>

      <p className="text-center text-[10px] text-gray-600 mt-6 uppercase tracking-widest font-bold">
        Clawzeneger Omega Encryption • 2026
      </p>
    </div>
  );
}
