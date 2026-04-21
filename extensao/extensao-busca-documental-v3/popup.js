async function verificarStatus() {
    console.log("=== INICIANDO verificarStatus() ===");

    const statusDiv = document.getElementById("status");
    console.log("statusDiv encontrado:", statusDiv);

    try {
        console.log("Tentando conectar com Python em localhost...");

        const response = await fetch("http://127.0.0.1:8765/status");
        console.log("Response recebida:", response);

        const data = await response.json();
        console.log("JSON recebido do Python:", data);

        if (data.status === "online") {
            console.log("Python está ONLINE");

            statusDiv.innerHTML =
                "Aplicação Python está ATIVA<br>" +
                "Lendo dados da tela...";

            statusDiv.style.color = "green";
        } else {
            console.log("Python respondeu mas não está online:", data);

            statusDiv.innerHTML =
                "Aplicação Python está INATIVA<br>" +
                "Não é possível ler os dados em tela!";

            statusDiv.style.color = "red";
        }

    } catch (error) {
        console.error("ERRO em verificarStatus():", error);

        statusDiv.innerHTML =
            "Aplicação Python está FECHADA<br>" +
            "Não é possível ler os dados em tela!";

        statusDiv.style.color = "red";
    }

    console.log("=== FINALIZANDO verificarStatus() ===");
}


async function lerDadosTela() {
    console.log("=== INICIANDO lerDadosTela() ===");

    const statusDiv = document.getElementById("status");
    const dadosDiv = document.getElementById("dados");

    console.log("statusDiv:", statusDiv);
    console.log("dadosDiv:", dadosDiv);

    try {
        console.log("Buscando aba ativa...");

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        console.log("Tab encontrada:", tab);

        if (!tab || !tab.id) {
            throw new Error("Não foi possível encontrar a aba ativa");
        }

        console.log("Executando script dentro da página...");

        const results = await chrome.scripting.executeScript({
            target: {
                tabId: tab.id
            },
            func: () => {
                console.log("=== EXECUTANDO DENTRO DA PÁGINA ===");

                const contaEl = document.getElementById(
                    "sys_display.sn_customerservice_case.account"
                );

                const moduloEl = document.getElementById(
                    "sys_display.sn_customerservice_case.u_module_function"
                );

                console.log("contaEl:", contaEl);
                console.log("moduloEl:", moduloEl);

                const contaValor = contaEl
                    ? contaEl.value.trim()
                    : null;

                const moduloValor = moduloEl
                    ? moduloEl.value.trim()
                    : null;

                console.log("contaValor:", contaValor);
                console.log("moduloValor:", moduloValor);

                return {
                    conta: contaValor,
                    modulo: moduloValor
                };
            }
        });

        console.log("Resultado do executeScript:", results);

        if (!results || !results.length) {
            throw new Error("Nenhum resultado retornado pelo executeScript");
        }

        const data = results[0].result;
        console.log("Data final recebida:", data);

        if (!data) {
            throw new Error("Data veio vazia");
        }

        if (!data.conta || !data.modulo) {
            console.error("Campos vazios:", data);
            throw new Error("Campos vazios");
        }

        console.log("Dados encontrados com sucesso!");

        dadosDiv.innerHTML = `
            <div>
                <strong>Conta:</strong><br>
                ${data.conta}
            </div>

            <div style="margin-top: 12px;">
                <strong>Módulo/Função:</strong><br>
                ${data.modulo}
            </div>
        `;

        console.log("HTML atualizado com sucesso");

    } catch (error) {
        console.error("ERRO em lerDadosTela():", error);

        statusDiv.innerHTML =
            "Aplicação Python está ATIVA<br>" +
            "Não é possível ler os dados em tela!";

        statusDiv.style.color = "red";

        dadosDiv.innerHTML = "";
    }

    console.log("=== FINALIZANDO lerDadosTela() ===");
}


console.log("=== EXTENSÃO INICIADA ===");

verificarStatus();
lerDadosTela();