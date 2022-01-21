import re
import json
from django.shortcuts import render
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from main.models import Policy
from main.api.serializers import PolicySerializer, PolicySearchSerializer
from main.api.serializers import PolicySpacySearchSerializer
from main.utils import transform_text, spacy_nlp


class PolicyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Policies.
    Use the /policy/search?q=your query to search by jaccard similarity
    """
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    
    def get_serializer_context(self):
        # Add the incoming search term to serializer to allow it to calculate jaccard etc.
        context = super().get_serializer_context()
        context.update(
            {
                "search_terms_set": set(self.get_search_terms(self.request))
            }
        )
        return context


    def get_search_terms(self, request):
        search_terms = self.request.query_params.get('q', "")  # ['agenda', 'mitigation']
        return transform_text(search_terms).split()
    
    @staticmethod
    def get_search_queryset(search_terms: list) -> QuerySet:
        """
        Query db for entries with search term words in
        """
        all_qs = Policy.objects.all()
        qs = all_qs if not search_terms else Policy.objects.none()
        if search_terms:
            escaped_terms = [f'[\\s^]{re.escape(n)}[\\s$]' for n in search_terms]
            result = Policy.objects.filter(terms__iregex=r'(' + '|'.join(escaped_terms) + ')')
        else:
            result = all_qs
        
        for s in search_terms:
            qs = (qs | all_qs.filter(terms__iregex=f'[^\\w]{s}[\\w$]'))
        return qs.distinct()

    @action(methods=['GET'], detail=False)
    def search(self, request):
        """
        End point for searching data, use q= space separated query
        """
        search_terms = self.get_search_terms(request)
        search_qs = self.get_search_queryset(search_terms)

        ordering = 'jaccard_similarity'
        context = {"search_terms_set": set(search_terms)}
        
        data = PolicySearchSerializer(search_qs, many=True, context=context).data
        data = sorted(data, key=lambda k: (k[ordering], ), reverse=True)
        return Response(data)

    @action(methods=['GET'], detail=False)
    def spacy_search(self, request):
        """Show spacy results"""
        if not spacy_nlp:
            return Response('Spacy not installed on this platform')
        print('1')
        search_terms_string = self.request.query_params.get('q', '')
        search_terms = self.get_search_terms(request)
        search_qs = self.get_search_queryset(search_terms)

        ordering = 'spacy_similarity'
        context = {"search_terms_nlp": spacy_nlp(search_terms)}
        print('2')
        data = PolicySpacySearchSerializer(search_qs, many=True, context=context).data
        data = sorted(data, key=lambda k: (k[ordering], ), reverse=True)
        return Response(data)