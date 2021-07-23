import utils.ma as ma_utils


class Product:
    def __init__(self, html):
        self.html = html
        self.__id = self.__scrape_id()
        self.__reference = self.__scrape_reference()
        self.__name = self.__scrape_name()
        self.__price = self.__scrape_price()
        self.__categories = self.__scrape_categories()
        self.__serial_number = self.__scrape_serial_number()
        self.__plate_number = self.__scrape_plate_number()
        self.__make_model = self.__scrape_make_model()
        self.__year_manufacture = self.__scrape_year_manufacture()
        self.__model_year = self.__scrape_model_year()
        self.__engine = self.__scrape_engine()
        self.__fuel_type = self.__scrape_fuel_type()
        self.__mileage = self.__scrape_mileage()
        self.__location = self.__scrape_location()
        self.__plant = self.__scrape_plant()
        self.__city = self.__scrape_city()
        self.__state = self.__scrape_state()
        self.__owner = self.__scrape_owner()
        self.__url = self.__scrape_url()
        self.__images = self.__scrape_images()
        self.__observations = self.__scrape_observations()

    def __scrape_id(self):
        try:
            element = self.html.find("input", attrs={"name": "comment_post_ID"})
            id = int(element["value"])
        except Exception:
            id = 0
        finally:
            return id

    def __scrape_reference(self):
        try:
            reference = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Código do equipamento" in element.string:
                    reference = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            reference = str(reference).replace("*", "A")
        except Exception:
            reference = ""
        finally:
            return reference

    def __scrape_name(self):
        try:
            name = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Descrição do equipamento" in element.string:
                    name = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            name = str(name).upper()
        except Exception:
            name = ""
        finally:
            return name

    def __scrape_price(self):
        try:
            price = ""
            for char in str(
                self.html.find("div", attrs={"class": "field-price"}).string
            ):
                if char.isdigit():
                    price = price + char
            price = float(price) / 100
        except Exception:
            price = float(0)
        finally:
            return price

    def __scrape_categories(self):
        try:
            categories = []
            elements = self.html.select("span.cat-links a")
            for element in elements:
                categories.append(element.string)
        except Exception:
            categories = ""
        finally:
            return categories

    def __scrape_serial_number(self):
        try:
            serial_number = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Número de série" in element.string:
                    serial_number = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            serial_number = str(serial_number)
        except Exception:
            serial_number = ""
        finally:
            return serial_number

    def __scrape_plate_number(self):
        try:
            plate_number = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Placa" in element.string:
                    plate_number = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            plate_number = str(plate_number)
        except Exception:
            plate_number = ""
        finally:
            return plate_number

    def __scrape_make_model(self):
        try:
            make_model = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Marca ou Modelo" in element.string:
                    make_model = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            make_model = str(make_model)
        except Exception:
            make_model = ""
        finally:
            return make_model

    def __scrape_year_manufacture(self):
        try:
            year_manufacture = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Ano de fabricação" in element.string:
                    year_manufacture = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            year_manufacture = int(year_manufacture)
        except Exception:
            year_manufacture = 0
        finally:
            return year_manufacture

    def __scrape_model_year(self):
        try:
            model_year = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Ano do modelo" in element.string:
                    model_year = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            model_year = int(model_year)
        except Exception:
            model_year = 0
        finally:
            return model_year

    def __scrape_engine(self):
        try:
            engine = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Motor" in element.string:
                    engine = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            engine = str(engine)
        except Exception:
            engine = ""
        finally:
            return engine

    def __scrape_fuel_type(self):
        try:
            fuel_type = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Combustível" in element.string:
                    fuel_type = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            fuel_type = str(fuel_type)
        except Exception:
            fuel_type = ""
        finally:
            return fuel_type

    def __scrape_mileage(self):
        try:
            mileage = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "KMs" in element.string:
                    mileage = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            mileage = str(mileage)
        except Exception:
            mileage = ""
        finally:
            return mileage

    def __scrape_location(self):
        try:
            location = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Localização atual" in element.string:
                    location = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            location = str(location)
        except Exception:
            location = ""
        finally:
            return location

    def __scrape_plant(self):
        try:
            plant = self.__location[0 : self.__location.index("(") - 1]
            plant = plant.replace(" -", "").strip()
        except Exception:
            try:
                plant = self.__location[0 : self.__location.index("-") - 1]
                plant = plant.replace(" -", "").strip()
            except Exception:
                plant = ""
        finally:
            return plant

    def __scrape_city(self):
        try:
            city_state = self.__location[
                self.__location.index("(") + 1 : self.__location.rindex(")")
            ]
            city = ma_utils.split_city_and_state(city_state)[0].strip()
        except Exception:
            try:
                city_state = self.__location.split("-")
                city = city_state[1].strip()
            except Exception:
                city = ""
        finally:
            return city

    def __scrape_state(self):
        try:
            city_state = self.__location[
                self.__location.index("(") + 1 : self.__location.rindex(")")
            ]
            state = ma_utils.split_city_and_state(city_state)[1].strip()
        except Exception:
            try:
                city_state = self.__location.split("-")
                state = city_state[2].strip()
            except Exception:
                state = ""
        finally:
            return state

    def __scrape_owner(self):
        try:
            owner = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Proprietário" in element.string:
                    owner = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            owner = str(owner)
        except Exception:
            owner = ""
        finally:
            return owner

    def __scrape_url(self):
        try:
            url = "https://vendas.queirozgalvao.com/?p=" + str(self.__id)
        except Exception:
            url = ""
        finally:
            return url

    def __scrape_images(self):
        try:
            images = []
            elements = self.html.select("img.slider-image")
            for element in elements:
                if element["src"] not in images:
                    images.append(element["src"])
        except Exception:
            images = []
        finally:
            return images

    def __scrape_observations(self):
        try:
            observations = ""
            elements = self.html.find_all("div", attrs={"class": "field-label"})
            for element in elements:
                if "Observações sobre o equipamento" in element.string:
                    observations = element.parent.find(
                        "div", attrs={"class": "field-value"}
                    ).string
            observations = str(observations)
        except Exception:
            observations = ""
        finally:
            return observations

    def get_id(self):
        return self.__id

    def get_reference(self):
        return self.__reference

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_categories(self):
        return self.__categories

    def get_category(self):
        if "Equipamentos" in self.__categories:
            return "Equipamentos"
        elif "Outros" in self.__categories:
            return "Outros"
        else:
            return ""

    def get_subcategory(self):
        categories = self.__categories.copy()

        if "Todas" in categories:
            categories.remove("Todas")
        if "Equipamentos" in categories:
            categories.remove("Equipamentos")
        if "Outros" in categories:
            categories.remove("Outros")

        return categories[0]

    def get_serial_number(self):
        return self.__serial_number

    def get_plate_number(self):
        return self.__plate_number

    def get_make_model(self):
        return self.__make_model

    def get_year_manufacture(self):
        return self.__year_manufacture

    def get_model_year(self):
        return self.__model_year

    def get_engine(self):
        return self.__engine

    def get_fuel_type(self):
        return self.__fuel_type

    def get_mileage(self):
        return self.__mileage

    def get_location(self):
        return self.__location

    def get_plant(self):
        return self.__plant

    def get_city(self):
        return self.__city

    def get_state(self):
        return self.__state

    def get_owner(self):
        return self.__owner

    def get_url(self):
        return self.__url

    def get_images(self):
        return self.__images

    def get_observations(self):
        return self.__observations

    def get_short_description(self):
        short_description = ""

        special_cases = ["Veículos", "Caminhões", "Ônibus", "Guindastes"]

        if self.get_subcategory() in special_cases:
            if self.get_name():
                short_description = short_description + self.get_name()

            if self.get_year_manufacture() and self.get_model_year():
                short_description = (
                    short_description
                    + ", "
                    + str(self.get_year_manufacture())
                    + "/"
                    + str(self.get_model_year())
                )
            elif self.get_year_manufacture():
                short_description = (
                    short_description + ", " + str(self.get_year_manufacture())
                )
            elif self.get_model_year():
                short_description = (
                    short_description + ", " + str(self.get_model_year())
                )

            if self.get_plate_number():
                short_description = (
                    short_description + ", PL.: " + self.get_plate_number()
                )

            if self.get_state():
                short_description = short_description + " (" + self.get_state() + ")"

            if self.get_serial_number():
                short_description = (
                    short_description + ", CH.: " + self.get_serial_number()
                )
        else:
            if self.get_name():
                short_description = short_description + self.get_name()

            if self.get_year_manufacture() and self.get_model_year():
                short_description = (
                    short_description
                    + ", ANO "
                    + str(self.get_year_manufacture())
                    + "/"
                    + str(self.get_model_year())
                )
            elif self.get_year_manufacture():
                short_description = (
                    short_description + ", ANO " + str(self.get_year_manufacture())
                )
            elif self.get_model_year():
                short_description = (
                    short_description + ", ANO " + str(self.get_model_year())
                )

            if self.get_serial_number():
                short_description = (
                    short_description + ", SÉRIE: " + self.get_serial_number()
                )

        return short_description.upper()

    def get_full_description(self):
        full_description = ""

        special_cases = ["Veículos", "Caminhões", "Ônibus", "Guindastes"]

        if self.get_subcategory() in special_cases:
            if self.get_name():
                full_description = (
                    full_description + "Nome: " + self.get_name() + "<br>"
                )

            if self.get_plate_number():
                full_description = (
                    full_description + "Placa: " + self.get_plate_number() + "<br>"
                )

            if self.get_state():
                full_description = (
                    full_description + " (" + self.get_state() + ")" + "<br>"
                )

            if self.get_serial_number():
                full_description = (
                    full_description + "Chassi: " + self.get_serial_number() + "<br>"
                )

            if self.get_year_manufacture() and self.get_model_year():
                full_description = (
                    full_description
                    + "Ano Fab/Modelo: "
                    + str(self.get_year_manufacture())
                    + "/"
                    + str(self.get_model_year())
                    + "<br>"
                )
            elif self.get_year_manufacture():
                full_description = (
                    full_description
                    + "Ano Fabricação: "
                    + str(self.get_year_manufacture())
                    + "<br>"
                )
            elif self.get_model_year():
                full_description = (
                    full_description
                    + "Ano Modelo: "
                    + str(self.get_model_year())
                    + "<br>"
                )

            if self.get_mileage():
                full_description = (
                    full_description + "Km acima de: " + self.get_mileage() + "<br>"
                )

            if self.get_fuel_type():
                full_description = (
                    full_description + "Combustível: " + self.get_fuel_type() + "<br>"
                )

            if self.get_make_model() and self.get_make_model() != self.get_name():
                full_description = (
                    full_description + "Marca/Modelo: " + self.get_make_model() + "<br>"
                )

            if self.get_engine():
                full_description = (
                    full_description + "Motor: " + self.get_engine() + "<br>"
                )

            if self.get_observations():
                full_description = (
                    full_description + "Obs: " + self.get_observations() + "<br>"
                )
        else:
            if self.get_name():
                full_description = (
                    full_description + "Nome: " + self.get_name() + "<br>"
                )

            if self.get_year_manufacture():
                full_description = (
                    full_description
                    + "Ano de fabricação: "
                    + str(self.get_year_manufacture())
                    + "<br>"
                )

            if self.get_model_year():
                full_description = (
                    full_description
                    + "Ano do modelo: "
                    + str(self.get_model_year())
                    + "<br>"
                )

            if self.get_serial_number():
                full_description = (
                    full_description
                    + "Número de série: "
                    + self.get_serial_number()
                    + "<br>"
                )

            if self.get_fuel_type():
                full_description = (
                    full_description + "Combustível: " + self.get_fuel_type() + "<br>"
                )

            if self.get_make_model() and self.get_make_model() != self.get_name():
                full_description = (
                    full_description
                    + "Espécie ou Marca ou Modelo: "
                    + self.get_make_model()
                    + "<br>"
                )

            if self.get_mileage():
                full_description = (
                    full_description
                    + "Horímetro acumulado: "
                    + self.get_mileage()
                    + "<br>"
                )

            if self.get_observations():
                full_description = (
                    full_description
                    + "Observações sobre o equipamento: "
                    + self.get_observations()
                    + "<br>"
                )

        return full_description

    def to_string(self):
        return "Produto: ID: {} - Referência: {} - Nome: {} - Preço: R$ {:.2f} - Categorias: {} - Categoria: {} - Subcategoria: {} - Número de Série: {} - Placa: {} - Marca e Modelo: {} - Ano de Fabricação: {} - Ano do Modelo: {} - Motor: {} - Combustível: {} - Quilometragem: {} - Localização: {} - Unidade: {} - Cidade: {} - Estado: {} - Responsável: {} - URL: {} - Qtd de Fotos: {} - Observações: {}".format(
            self.get_id(),
            self.get_reference(),
            self.get_name(),
            self.get_price(),
            self.get_categories(),
            self.get_category(),
            self.get_subcategory(),
            self.get_serial_number(),
            self.get_plate_number(),
            self.get_make_model(),
            self.get_year_manufacture(),
            self.get_model_year(),
            self.get_engine(),
            self.get_fuel_type(),
            self.get_mileage(),
            self.get_location(),
            self.get_plant(),
            self.get_city(),
            self.get_state(),
            self.get_owner(),
            self.get_url(),
            len(self.get_images()),
            len(self.get_observations()),
        )
