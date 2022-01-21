from logging import getLogger
from main.models import Policy, Sector
from rest_framework import serializers
from main.utils import spacy_nlp

log = getLogger(__name__)


try:
    import spacy
    nlp = spacy.load("en_core_web_md")
except ImportError:
    nlp = None


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ['name']


class PolicySerializer(serializers.ModelSerializer):
    sectors = SectorSerializer(many=True)  # serializers.SerializerMethodField()

    def create(self, validated_data):
        sectors = validated_data.pop('sectors', [])
        policy = Policy.objects.create(**validated_data)
        for s in sectors:
            Sector.objects.get_or_create(name=s)
        return policy

    def update(self, instance, validated_data):
        request = self.context.get('request')
        data = request.data.copy()
        sectors = validated_data.pop('sectors', [])
        if sectors:
            sectors = [(Sector.objects.get_or_create(name=s['name']))[0] for s in sectors]
            self.instance.sectors.set(sectors)
            self.instance.save()
        super().update(instance, validated_data)
        return instance

    def get_sectors(self, instance):
        return [s.name for s in instance.sectors.all()]

    class Meta:
        model = Policy
        fields = ['id','title', 'sectors', 'description_text'] # '__all__'


class PolicySearchSerializer(PolicySerializer):
    jaccard_similarity = serializers.SerializerMethodField()

    def get_jaccard_similarity(self, instance):
        sts = self.context['search_terms_set']
        terms = instance.terms.split()
        union_length = len((sts.union(terms)))
        j_c = len(sts.intersection(terms)) / union_length if union_length else 0.0
        return j_c 

    class Meta:
        model = Policy
        fields = ['id','title', 'sectors', 'description_text', 'jaccard_similarity'] # '__all__'


class PolicySpacySearchSerializer(PolicySerializer):
    spacy_similarity = serializers.SerializerMethodField()

    def get_spacy_similarity(self, instance):
        if not spacy_nlp:
            return 0.0
        search_terms_nlp = self.context['search_terms_nlp']
        desc_nlp = spacy_nlp(instance.description_text)
        # terms_nlp = spacy_nlp(instance.terms)
        s_s = search_terms_nlp.similarity(desc_nlp)
        # s_s = search_terms_nlp.similarity(terms_nlp)
        log.debug('ss: ' , s_s)
        return s_s

    class Meta:
        model = Policy
        fields = ['id','title', 'sectors', 'description_text', 'spacy_similarity'] # '__all__'
