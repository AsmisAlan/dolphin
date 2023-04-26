from typing import List, Tuple
from autoscraper import AutoScraper


class AutoScrapperConfiguration:
    def __init__(self, group_by_alias: bool, models: List[Tuple[str, List[str]]]):
        self.group_by_alias = group_by_alias
        self.models = models

    def add_model(self, url: str, find: List[str]):
        self.models.append((url, find))


class AutoScrapperInput:
    def __init__(self, url):
        self.url = url


class AutoScrapperOutput:
    def __init__(self) -> None:
        pass


def auto_scrapper(configuration: AutoScrapperConfiguration, input: AutoScrapperInput) -> AutoScrapperOutput:
    scrapper = AutoScraper()

    for c in configuration.models:
        scrapper.build(url=c[0], wanted_list=c[1], update=True)

    return scrapper.get_result_exact(url=input.url)


if __name__ == "__main__":
    # Get the data from the page
    configuration = AutoScrapperConfiguration(
        True, [])

    configuration.add_model("https://articulo.mercadolibre.com.ar/MLA-1121146078-banco-hamaca-sillon-colgante-de-jardin-plaza-exterior-_JM?variation=174140864584#reco_item_pos=2&reco_backend=machinalis-homes-pdp-boos&reco_backend_type=function&reco_client=home_navigation-recommendations&reco_id=4d85f31a-0068-479a-8e09-13ff53e219d1&c_id=/home/navigation-recommendations/element&c_element_order=3&c_uid=3782d015-fe25-4e2d-8b1e-20625c375f67", [
                            "Banco Hamaca Sillon Colgante De Jardin Plaza Exterior", "83.629", "35% OFF", "128.660"])

    configuration.add_model("https://articulo.mercadolibre.com.ar/MLA-1339853899-juego-de-comedor-mesa-6-sillas-madera-brandson-_JM?variation=176552775205#reco_item_pos=1&reco_backend=machinalis-seller-items-pdp&reco_backend_type=low_level&reco_client=vip-seller_items-above&reco_id=06b74aa8-5151-4777-be19-198707ec03e9", [
                            "Juego De Comedor Mesa + 6 Sillas Madera Brandson", "213.426", "40% OFF", "355.710"])

    configuration.add_model("https://articulo.mercadolibre.com.ar/MLA-1339853899-juego-de-comedor-mesa-6-sillas-madera-brandson-_JM?variation=176552775205#reco_item_pos=1&reco_backend=machinalis-seller-items-pdp&reco_backend_type=low_level&reco_client=vip-seller_items-above&reco_id=06b74aa8-5151-4777-be19-198707ec03e9", [
                            "Sillón Hamaca Nido", "45.000"])

    configuration.add_model("https://www.mercadolibre.com.ar/smart-tv-noblex-dk43x7100pi-led-43-full-hd-con-android-tv/p/MLA19712050?pdp_filters=deal:MLA779357-1&hide_psmb=true#searchVariation=MLA19712050&position=2&search_layout=grid&type=product&tracking_id=af595dda-9d76-4553-8807-7a380da01555&deal_print_id=c59cdd6e-f4d0-4304-be46-47dd945c32f0&promotion_type=DEAL_OF_THE_DAY", [
                            "Smart Tv Noblex Dk43x7100pi Led 43'' Full Hd Con Android Tv", "89.999", "18% OFF", "109.999"])

    input = AutoScrapperInput(
        url="https://articulo.mercadolibre.com.ar/MLA-1361007460-televisor-_JM#position=3&search_layout=stack&type=item&tracking_id=0401003f-7ecb-45cd-94bb-d91a34aa10d3")
    output = auto_scrapper(configuration, input)
    print(f"Text: {output}")
