from playwright.sync_api import Page, expect


class PlaywrightUtils:
    """
    Utility class with common functions for automation using Playwright.
    """

    def __init__(self, page: Page):
        self.page = page

    # -------------------------
    # Navigation
    # -------------------------
    def open_url(self, url: str):
        """Abre uma URL."""
        self.page.goto(url)

    def go_back_page(self):
        """Volta para a página anterior."""
        self.page.go_back()

    def go_forward_page(self):
        """Avança para a próxima página."""
        self.page.go_forward()

    def reload_page(self):
        """Recarrega a página atual."""
        self.page.reload()

    # -------------------------
    # Waits
    # -------------------------
    def wait_timeout(self, tempo_ms: int):
        """Espera um tempo fixo em milissegundos."""
        self.page.wait_for_timeout(tempo_ms)

    def wait_element(self, seletor: str, timeout: int = 10000):
        """Espera um elemento aparecer."""
        self.page.wait_for_selector(seletor, timeout=timeout)

    def wait_url(self, url: str):
        """Espera a URL mudar."""
        self.page.wait_for_url(url)

    def wait_load(self):
        """Espera o carregamento completo da página."""
        self.page.wait_for_load_state("networkidle")

    # -------------------------
    # Interactions
    # -------------------------
    def click(self, seletor: str):
        """Clica em um elemento."""
        self.page.locator(seletor).click()

    def double_click(self, seletor: str):
        """Executa duplo clique."""
        self.page.locator(seletor).dblclick()

    def fill(self, seletor: str, texto: str):
        """Preenche um campo."""
        self.page.locator(seletor).fill(texto)

    def type_text(self, seletor: str, texto: str, delay: int = 50):
        """Digita texto simulando teclado."""
        self.page.locator(seletor).type(texto, delay=delay)

    def press_key(self, tecla: str):
        """Pressiona uma tecla."""
        self.page.keyboard.press(tecla)

    def hover(self, seletor: str):
        """Move o mouse sobre um elemento."""
        self.page.locator(seletor).hover()

    def scroll_to_element(self, seletor: str):
        """Rola até o elemento."""
        self.page.locator(seletor).scroll_into_view_if_needed()

    # -------------------------
    # Capture and Files
    # -------------------------
    def screenshot_page(self, caminho: str = "pagina.png"):
        """Captura screenshot da página inteira."""
        self.page.screenshot(path=caminho, full_page=True)

    def screenshot_element(self, seletor: str, caminho: str):
        """Captura screenshot de um elemento."""
        self.page.locator(seletor).screenshot(path=caminho)

    def save_pdf(self, caminho: str = "arquivo.pdf"):
        """Salva a página em PDF."""
        self.page.pdf(path=caminho)

    # -------------------------
    # Get Information
    # -------------------------
    def get_text(self, seletor: str) -> str:
        """Retorna o texto de um elemento."""
        return self.page.locator(seletor).inner_text()
    
    def get_locator(self, seletor: str) -> str:
        """Retorna o texto de um elemento."""
        return self.page.locator(seletor)
    
    def get_locator_visible(self, seletor: str) -> str:
        """Retorna o texto de um elemento."""
        return self.page.locator(seletor).is_visible()
    
    def get_text_by_pos(self, seletor: str, pos: int, parent_element: bool=False) -> str:
        """Retorna o texto de um elemento baseado em sua posição"""
        if not parent_element:
            return self.page.locator(seletor).nth(pos).inner_text()
        return self.page.locator(seletor).locator("..").nth(pos).inner_text()

    def get_value(self, seletor: str) -> str:
        """Retorna o valor de um campo."""
        return self.page.locator(seletor).input_value()

    def get_html(self, seletor: str) -> str:
        """Retorna o HTML interno."""
        return self.page.locator(seletor).inner_html()

    def get_title(self) -> str:
        """Retorna o título da página."""
        return self.page.title()

    def get_url(self) -> str:
        """Retorna a URL atual."""
        return self.page.url

    # -------------------------
    # Validations
    # -------------------------
    def validate_text(self, seletor: str, texto_esperado: str):
        """Valida texto de um elemento."""
        expect(self.page.locator(seletor)).to_have_text(texto_esperado)
        
    def has_text(self, seletor: str, texto_esperado: str) -> bool:
        try:
            texto = self.page.locator(seletor).inner_text(timeout=4000)
            return texto_esperado in texto
        except:
            return False

    def validate_visible(self, seletor: str):
        """Valida se elemento está visível."""
        expect(self.page.locator(seletor)).to_be_visible()

    def validate_hidden(self, seletor: str):
        """Valida se elemento está oculto."""
        expect(self.page.locator(seletor)).not_to_be_visible()

    def validate_url(self, url_esperada: str):
        """Valida URL atual."""
        expect(self.page).to_have_url(url_esperada)

    # -------------------------
    # Frames
    # -------------------------
    def access_frame(self, frame_name: str):
        """Retorna um frame pelo nome."""
        return self.page.frame(name=frame_name)

    # -------------------------
    # JavaScript
    # -------------------------
    def execute_js(self, script: str):
        """Executa JavaScript na página."""
        return self.page.evaluate(script)

    # -------------------------
    # Dropdown
    # -------------------------
    def select_dropdown(self, seletor: str, valor: str):
        """Seleciona valor em um dropdown."""
        self.page.locator(seletor).select_option(valor)

    # -------------------------
    # Checkbox
    # -------------------------
    def check_checkbox(self, seletor: str):
        """Marca um checkbox."""
        self.page.locator(seletor).check()

    def uncheck_checkbox(self, seletor: str):
        """Desmarca um checkbox."""
        self.page.locator(seletor).uncheck()

...