async function lerDadosTela() {
    const statusDiv = document.getElementById("status");
    const dadosDiv = document.getElementById("dados");

    try {
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        if (!tab || !tab.id) {
            throw new Error("Aba ativa não encontrada");
        }

        const results = await chrome.scripting.executeScript({
            target: {
                tabId: tab.id
            },
            func: () => {
                // Primeiro seleciona a seção desejada
                const secao = document.querySelector(
                    '.tabs2_section.tabs2_section_0.tabs2_section0'
                );

                if (secao) {
                    // Simula clique para abrir/ativar a aba
                    secao.click();
                }

                // Após selecionar a aba, busca os campos
                const conta = document.getElementById(
                    "sys_display.sn_customerservice_case.account"
                )?.value;

                const funcao = document.getElementById(
                    "sys_display.sn_customerservice_case.u_module_function"
                )?.value;

                return {
                    conta,
                    funcao
                };
            }
        });

        const data = results?.[0]?.result;

        if (!data) {
            throw new Error("Nenhum dado retornado");
        }

        dadosDiv.innerHTML = `
            <div style="margin-bottom: 12px;">
                <strong>CONTA:</strong><br>
                ${data.conta || "Não encontrado"}
            </div>

            <div>
                <strong>FUNÇÃO:</strong><br>
                ${data.funcao || "Não encontrado"}
            </div>
        `;

        statusDiv.innerHTML =
            "Aplicação Python está ATIVA<br>" +
            "Dados carregados com sucesso!";

        statusDiv.style.color = "green";

    } catch (error) {
        console.error(error);

        statusDiv.innerHTML =
            "Não é possível ler os dados em tela!";

        statusDiv.style.color = "red";
        dadosDiv.innerHTML = "";
    }
}

lerDadosTela();