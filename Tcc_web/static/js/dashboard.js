/**
 * Dashboard de Ocorrências - JavaScript
 * Caminho: C:\xampp\htdocs\tccxampp\static\js\dashboard.js
 */

const API_BASE = 'http://localhost/tccxampp/api.php';

// =============================================
// INICIALIZAÇÃO
// =============================================
document.addEventListener('DOMContentLoaded', function () {
    carregarEstatisticas();
    carregarOcorrencias();
    carregarFiltros();
    configurarEventos();
});

// =============================================
// ESTATÍSTICAS
// =============================================
function carregarEstatisticas() {
    fetch(API_BASE + '?acao=estatisticas')
        .then(r => r.json())
        .then(dados => {
            if (dados.erro) return;
            var d = dados.dados;
            var el;
            el = document.getElementById('totalOcorrencias');
            if (el) el.textContent = d.total;
            el = document.getElementById('totalAndamento');
            if (el) el.textContent = d.em_andamento;
            el = document.getElementById('totalSolucionadas');
            if (el) el.textContent = d.solucionadas;

            popularFiltro('filtroTipo', d.categorias, 'categoria');
            popularFiltro('filtroBairro', d.bairros, 'bairro');
            renderizarGraficoTipos(d.categorias);
        })
        .catch(function(err){ console.error('Erro estatísticas:', err); });
}

// =============================================
// CARREGAR OCORRÊNCIAS
// =============================================
function carregarOcorrencias(params) {
    var loading    = document.getElementById('loading');
    var erroMsg    = document.getElementById('erroMsg');
    var semDados   = document.getElementById('semDados');
    var tabela     = document.getElementById('tabelaOcorrencias');
    var corpo      = document.getElementById('corpoTabela');

    if (loading) loading.classList.remove('d-none');
    if (erroMsg) erroMsg.classList.add('d-none');
    if (semDados) semDados.classList.add('d-none');
    if (tabela) tabela.style.display = 'none';

    var url = API_BASE + '?acao=lista' + (params ? '&' + params : '');

    fetch(url)
        .then(function(r){ if(!r.ok) throw new Error('Erro'); return r.json(); })
        .then(function(dados){
            if (loading) loading.classList.add('d-none');
            if (dados.erro) { mostrarErro(dados.mensagem || 'Erro ao carregar.'); return; }

            var lista = dados.dados || [];
            var cnt = document.getElementById('contadorResultados');
            if (cnt) cnt.textContent = lista.length + ' resultado' + (lista.length !== 1 ? 's' : '');

            if (lista.length === 0) {
                if (semDados) semDados.classList.remove('d-none');
                return;
            }

            if (!corpo) return;
            corpo.innerHTML = '';
            lista.forEach(function(oc){
                var statusClass = oc.status === 'Solucionada' ? 'badge-solucionada' : 'badge-em-andamento';
                var data = formatarData(oc.data_ocorrencia);
                var desc = oc.descricao
                    ? (oc.descricao.length > 60 ? oc.descricao.substring(0, 60) + '...' : oc.descricao)
                    : '<em class="text-muted">Sem descrição</em>';

                var tr = document.createElement('tr');
                tr.innerHTML =
                    '<td><strong>' + escapeHtml(oc.protocolo || '-') + '</strong></td>' +
                    '<td>' + escapeHtml(oc.categoria || '-') + '</td>' +
                    '<td><i class="fas fa-map-marker-alt text-danger me-1"></i>' + escapeHtml(oc.bairro || '-') + '</td>' +
                    '<td><small class="text-muted">' + data + '</small></td>' +
                    '<td><span class="badge ' + statusClass + '">' + escapeHtml(oc.status) + '</span></td>' +
                    '<td class="text-center"><button class="btn btn-sm btn-outline-primary btn-ver-detalhes" onclick="abrirDetalhe(' + oc.id + ')"><i class="fas fa-eye me-1"></i>Detalhes</button></td>';
                corpo.appendChild(tr);
            });

            if (tabela) tabela.style.display = 'table';
        })
        .catch(function(err){
            if (loading) loading.classList.add('d-none');
            mostrarErro('Não foi possível carregar as ocorrências. Verifique se o banco de dados está disponível.');
            console.error(err);
        });
}

// =============================================
// DETALHE (para página dedicada detalhe.php)
// =============================================
function carregarDetalhe(id) {
    var loading = document.getElementById('loadingDetalhe');
    var erro    = document.getElementById('erroDetalhe');
    var conteudo = document.getElementById('conteudoDetalhe');
    if (!loading) return;

    loading.classList.remove('d-none');
    if (erro) erro.classList.add('d-none');
    if (conteudo) conteudo.classList.add('d-none');

    fetch(API_BASE + '?acao=detalhe&id=' + id)
        .then(function(r){ if(!r.ok) throw new Error('Não encontrada'); return r.json(); })
        .then(function(dados){
            loading.classList.add('d-none');
            if (dados.erro) {
                document.getElementById('erroDetalheTexto').textContent = dados.mensagem;
                erro.classList.remove('d-none');
                return;
            }
            preencherDetalhe(dados.dados, 'conteudoDetalhe');
        })
        .catch(function(err){
            loading.classList.add('d-none');
            document.getElementById('erroDetalheTexto').textContent = 'Não foi possível carregar os detalhes.';
            erro.classList.remove('d-none');
        });
}

// =============================================
// DETALHE EM MODAL (para index.php / ocorrencias.php)
// =============================================
function abrirDetalhe(id) {
    var modal = new bootstrap.Modal(document.getElementById('modalDetalhe'));
    modal.show();
    var corpo = document.getElementById('corpoModal');
    corpo.innerHTML = '<div class="text-center py-4"><div class="spinner-border text-primary"></div></div>';

    fetch(API_BASE + '?acao=detalhe&id=' + id)
        .then(function(r){ if(!r.ok) throw new Error(); return r.json(); })
        .then(function(dados){
            if (dados.erro) { corpo.innerHTML = '<div class="alert alert-danger">' + dados.mensagem + '</div>'; return; }
            var d = dados.dados;
            var sc = d.status === 'Solucionada' ? 'badge-solucionada' : 'badge-em-andamento';
            var midia = '';
            if (d.foto && d.foto.trim() !== '') {
                var fotoUrl = d.foto.startsWith('http') ? d.foto : '../uploads/' + d.foto;
                midia = '<div class="col-12 mt-3"><h6><i class="fas fa-camera me-2"></i>Mídia</h6>' +
                    '<div class="galeria-item" onclick="ampliarImagem(\'' + escapeHtml(fotoUrl) + '\')">' +
                    '<img src="' + escapeHtml(fotoUrl) + '" alt="Foto" style="max-height:300px;width:100%;object-fit:cover;" ' +
                    'onerror="this.parentElement.innerHTML=\'<div class=alert alert-info>Imagem não encontrada</div>\'">' +
                    '</div></div>';
            }
            corpo.innerHTML =
                '<div class="row align-items-center mb-3"><div class="col"><h4 class="mb-0">' + escapeHtml(d.protocolo) + '</h4>' +
                '<span class="text-muted"><i class="fas fa-map-marker-alt me-1"></i>' + escapeHtml(d.bairro) + '</span></div>' +
                '<div class="col-auto"><span class="badge fs-6 ' + sc + '">' + escapeHtml(d.status) + '</span></div></div><hr>' +
                '<div class="row g-3">' +
                '<div class="col-md-6"><table class="table table-borderless table-sm">' +
                '<tr><td class="text-muted fw-bold" style="width:40%">Protocolo</td><td>' + escapeHtml(d.protocolo||'-') + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">Tipo</td><td>' + escapeHtml(d.categoria||'-') + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">Bairro</td><td>' + escapeHtml(d.bairro||'-') + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">Data</td><td>' + formatarData(d.data_ocorrencia) + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">Criado em</td><td>' + formatarDataHora(d.data_criacao) + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">Status</td><td><span class="badge ' + sc + '">' + escapeHtml(d.status) + '</span></td></tr>' +
                '<tr><td class="text-muted fw-bold">Anônimo</td><td>' + (d.anonimo == 1 ? 'Sim' : 'Não') + '</td></tr></table></div>' +
                '<div class="col-md-6"><h6>Denunciante</h6><table class="table table-borderless table-sm">' +
                '<tr><td class="text-muted fw-bold" style="width:40%">Nome</td><td>' + escapeHtml(d.nome_usuario||'-') + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">Telefone</td><td>' + escapeHtml(d.telefone_usuario||'-') + '</td></tr>' +
                '<tr><td class="text-muted fw-bold">E-mail</td><td>' + escapeHtml(d.email_usuario||'-') + '</td></tr></table></div>' +
                '<div class="col-12"><h6>Descrição</h6><p>' + escapeHtml(d.descricao||'Sem descrição') + '</p></div>' +
                midia + '</div>';
        })
        .catch(function(err){ corpo.innerHTML = '<div class="alert alert-danger">Não foi possível carregar os detalhes.</div>'; });
}

// =============================================
// PREENCHER DETALHE (usado na página dedicada)
// =============================================
function preencherDetalhe(d, containerId) {
    var sc = d.status === 'Solucionada' ? 'badge-solucionada' : 'badge-em-andamento';
    setText('detProtocolo', d.protocolo);
    setText('detBairroCab', d.bairro);
    setText('detProtocoloInfo', d.protocolo);
    setText('detCategoria', d.categoria);
    setText('detBairroInfo', d.bairro);
    setText('detData', formatarData(d.data_ocorrencia));
    setText('detDataCriacao', formatarDataHora(d.data_criacao));
    setText('detStatusInfo', d.status);
    setText('detAnonimo', d.anonimo == 1 ? 'Sim' : 'Não');
    setText('detNomeUsuario', d.nome_usuario || '-');
    setText('detTelefone', d.telefone_usuario || '-');
    setText('detEmail', d.email_usuario || '-');
    setText('detDescricao', d.descricao || 'Sem descrição');

    var badge = document.getElementById('detStatusBadge');
    if (badge) { badge.className = 'badge fs-6 ' + sc; badge.textContent = d.status; }

    // Mídia
    var secao = document.getElementById('secaoMidia');
    var galeria = document.getElementById('galeriaMidia');
    if (secao && galeria) {
        galeria.innerHTML = '';
        if (d.foto && d.foto.trim() !== '') {
            secao.style.display = 'block';
            var fotoUrl = d.foto.startsWith('http') ? d.foto : '../uploads/' + d.foto;
            var col = document.createElement('div');
            col.className = 'col-md-6 col-lg-4 mb-3';
            col.innerHTML = '<div class="galeria-item" onclick="ampliarImagem(\'' + escapeHtml(fotoUrl) + '\')">' +
                '<img src="' + escapeHtml(fotoUrl) + '" alt="Foto" onerror="this.alt=\'Imagem não encontrada\'"></div>';
            galeria.appendChild(col);
        } else {
            secao.style.display = 'none';
        }
    }

    document.getElementById(containerId).classList.remove('d-none');
}

// =============================================
// FILTROS
// =============================================
function carregarFiltros() {
    // Filtros são populados pelas estatísticas
}

function popularFiltro(id, dados, campo) {
    var sel = document.getElementById(id);
    if (!sel || !dados) return;
    sel.innerHTML = '<option value="">Todos</option>';
    dados.forEach(function(item){
        var opt = document.createElement('option');
        opt.value = item[campo];
        opt.textContent = item[campo] + ' (' + item.qtd + ')';
        sel.appendChild(opt);
    });
}

function montarParams() {
    var p = [];
    var busca     = document.getElementById('busca');
    var status    = document.getElementById('filtroStatus');
    var tipo      = document.getElementById('filtroTipo');
    var bairro    = document.getElementById('filtroBairro');
    var dataIni   = document.getElementById('dataInicio');
    var dataFim   = document.getElementById('dataFim');

    if (busca  && busca.value.trim())   p.push('busca=' + encodeURIComponent(busca.value.trim()));
    if (status && status.value)          p.push('status=' + encodeURIComponent(status.value));
    if (tipo   && tipo.value)            p.push('tipo=' + encodeURIComponent(tipo.value));
    if (bairro && bairro.value)          p.push('bairro=' + encodeURIComponent(bairro.value));
    if (dataIni && dataIni.value)        p.push('data_inicio=' + dataIni.value);
    if (dataFim && dataFim.value)        p.push('data_fim=' + dataFim.value);

    return p.join('&');
}

// =============================================
// EVENTOS
// =============================================
function configurarEventos() {
    var btn = document.getElementById('btnFiltrar');
    if (btn) btn.addEventListener('click', function(){ carregarOcorrencias(montarParams()); });

    var limpar = document.getElementById('btnLimpar');
    if (limpar) limpar.addEventListener('click', function(){
        ['busca','filtroStatus','filtroTipo','filtroBairro','dataInicio','dataFim'].forEach(function(id){
            var el = document.getElementById(id);
            if (el) el.value = '';
        });
        carregarOcorrencias();
    });

    var busca = document.getElementById('busca');
    if (busca) busca.addEventListener('keypress', function(e){
        if (e.key === 'Enter') { e.preventDefault(); carregarOcorrencias(montarParams()); }
    });
}

// =============================================
// GRÁFICO SIMPLES (barras com CSS)
// =============================================
function renderizarGraficoTipos(categorias) {
    var el = document.getElementById('graficoTipos');
    if (!el || !categorias || categorias.length === 0) { if(el) el.textContent = 'Sem dados'; return; }
    var max = Math.max.apply(null, categorias.map(function(c){ return parseInt(c.qtd); }));
    var html = '<div class="text-start">';
    var cores = ['#0d6efd','#198754','#ffc107','#dc3545','#6f42c1','#0dcaf0'];
    categorias.forEach(function(c, i){
        var pct = (parseInt(c.qtd) / max) * 100;
        html += '<div class="mb-2">' +
            '<div class="d-flex justify-content-between"><span>' + escapeHtml(c.categoria) + '</span><span class="fw-bold">' + c.qtd + '</span></div>' +
            '<div class="progress" style="height:22px;"><div class="progress-bar" role="progressbar" style="width:' + pct + '%;background-color:' + cores[i % cores.length] + '">' + c.qtd + '</div></div></div>';
    });
    html += '</div>';
    el.innerHTML = html;
}

// =============================================
// AMPLIAR IMAGEM
// =============================================
function ampliarImagem(url) {
    var img = document.getElementById('imgAmpliada');
    if (img) {
        img.src = url;
        new bootstrap.Modal(document.getElementById('modalImagem')).show();
    }
}

// =============================================
// UTILITÁRIOS
// =============================================
function formatarData(s) {
    if (!s) return '-';
    var p = s.split('-');
    return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : s;
}

function formatarDataHora(s) {
    if (!s) return '-';
    var clean = s.replace('T', ' ');
    var parts = clean.split(' ');
    var dp = parts[0].split('-');
    return dp.length === 3 ? dp[2] + '/' + dp[1] + '/' + dp[0] + ' ' + (parts[1] || '') : s;
}

function escapeHtml(t) {
    if (!t) return '';
    var d = document.createElement('div');
    d.textContent = t;
    return d.innerHTML;
}

function setText(id, val) {
    var el = document.getElementById(id);
    if (el) el.textContent = val || '-';
}

function mostrarErro(msg) {
    var e = document.getElementById('erroMsg');
    var t = document.getElementById('erroTexto');
    if (e && t) { t.textContent = msg; e.classList.remove('d-none'); }
}
